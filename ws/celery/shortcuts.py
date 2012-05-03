###############################################################################
#  Copyright 2011,2012 GISA Elkartea.                                         #
#                                                                             #
#  This file is part of django-ws.                                            #
#                                                                             #
#  django-ws is free software: you can redistribute it and/or modify it       #
#  under the terms of the GNU Affero General Public License as published      #
#  by the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                        #
#                                                                             #
#  django-ws is distributed in the hope that it will be useful, but WITHOUT   #
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or      #
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public       #
#  License for more details.                                                  #
#                                                                             #
#  You should have received a copy of the GNU Affero General Public License   #
#  along with django-ws. If not, see <http://www.gnu.org/licenses/>.          #
###############################################################################

from django.db.models import Count
from ws.models import Task, Process, Node


def assert_one_in_queryset(queryset):
    """Assert that queryset contains one object.

    Raise :exc:`django.core.exceptions.DoesNotExist` if queryset is empty,
    raise :exc:`django.core.exceptions.MultipleObjectsReturned` if more than
    one.
    """

    num = queryset.count()
    if num == 0:
        raise queryset.model.DoesNotExist
    elif num > 1:
        raise queryset.model.MultipleObjectsReturned
    else:
        return True


def update_task(pk=None, task_id=None, **kwargs):
    """ Get task with pk primary key or task_id task id, update it's
    values with ones specified in kwargs and return it.
    """

    if (pk, task_id) == (None, None):
        raise ValueError('pk or task_id argument must be passed.')

    if pk is not None:
        task_q = Task.objects.select_for_update().filter(pk=pk)
    elif task_id is not None:
        task_q = Task.objects.select_for_update().filter(task_id=task_id)

    assert_one_in_queryset(task_q)
    if task_id is not None:
        kwargs['task_id'] = task_id
    task_q.update(**kwargs)
    return task_q[0]


def update_process(pk, **kwargs):
    """Get process with pk primary key, update it's values with the ones
    specified in kwargs and return it.

    If the process is a subprocess, update the parent task too.
    """

    process_q = Process.objects.select_for_update().filter(pk=pk)
    assert_one_in_queryset(process_q)
    process_q.update(**kwargs)
    process = process_q[0]

    if process.parent:
        try:
            result = Task.objects.get(process=process, 
                    node__is_end=True).result
        except Task.DoesNotExist:
            result = ''
        update_task(process.parent.pk, state=process.state, result=result,
                start_date=process.start_date, end_date=process.end_date)
    return process


def is_launchable(node, process):
    """Decide whether a node can be launched or not.

    For a node to be possible to launch, it must have a number of successful
    parent transitions:

    with no parent transitions:
        0 must be fulfilled
    with a 'XOR' join:
        1 must be fulfilled
    with an 'AND' join:
        all parent transitions must be fulfilled
    """

    # All the successful parent tasks of the node
    parent_tasks = process.task_set.select_related().filter(state='SUCCESS')

    # Number of parent transitions
    num_parent_transitions = node.parent_transition_set.count()

    completed = 0
    # Number of parent transitions that must be fulfilled
    if num_parent_transitions == 0:
        must_complete = 0
    elif node.join == 'XOR':
        must_complete = 1
    else:
        must_complete = num_parent_transitions

    # For every parent transitions of the node
    for parent_transition in node.parent_transition_set.iterator():

        # If it has a successful task with his result met as parent
        if parent_tasks.filter(node=parent_transition.parent,  result__in=(
            '', parent_transition.condition)):

            completed += 1
            if completed == must_complete:
                break

    return completed == must_complete



def get_pending_childs(task):
    """Return the list of workflow nodes that must be launched when a task
    finishes. If task's node's split mode is XOR, only first found child node
    is returned.
    """
    childs = []
    process = task.process

    # Childs transitions that have their condition met
    transitions = task.node.child_transition_set.filter(
            condition__in=('', task.result))

    for transition in transitions.iterator():
        node = transition.child
        if is_launchable(node, process):
            childs.append(node)
            if childs and task.node.split == 'XOR':
                return childs
    return childs


def get_revocable_parents(task):
    """Return revocable parents for a started child.

    If a child has been already started, return it's parents that hasn't
    already finished, if this parents has not any other child.
    """

    if task.state != 'STARTED':
        return task.process.task_set.none()
    else:
        parent_transitions = task.node.parent_transition_set.iterator()
        return task.process.task_set.filter(state='STARTED',
                node__child_transition_set__in=parent_transitions).annotate(
                        child_num=Count('node__child_transition_set')).filter(
                                child_num=1)


def get_alternative_way(task):
    """Find another node in the workflow that can be started."""
    ways = [task.node]
    while ways:
        way = ways.pop()
        parent_transitions = way.parent_transition_set.filter(split='XOR')
        siblings = Node.objects.filter(
                parent_transition_set=parent_transitions)

        for sibling in siblings:
            if is_launchable(sibling, task.process):
                return sibling

        parents = Node.objects.filter(child_transition_set=parent_transitions)
        ways.append(parents)
    return None
