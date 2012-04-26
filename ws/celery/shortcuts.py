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
from ws.models import Task, Process


def update_process(pk, **kwargs):
    """ Get process with pk primary key and update it's values with ones
    specified in kwargs.
    
    Returns the updated process or None if no process found."""
    process_q = Process.objects.select_for_update().filter(pk=pk)
    process_q.select_for_update().update(**kwargs)
    if process_q:
        return process_q[0]
    return None


def update_task(pk=None, task_id=None, **kwargs):
    """ Get task with pk primary key or task_id task idand update it's
    values with ones specified in kwargs. One of pk or task_id must be
    passed, raises ValueError otherwise.
    
    Returns the updated task or None if no task found."""
    if pk is not None:
        task_q = Task.objects.select_for_update().filter(pk=pk)
    elif task_id is not None:
        task_q = Task.objects.select_for_update().filter(task_id=task_id)
    else:
        raise ValueError("One of pk or task_id argument must be passed.")
    task_q.select_for_update().update(**kwargs)
    if task_q:
        return task_q[0]
    return None


def update_parent(task):
    """ Update task's parent with task's values. It updates state, result,
    start_date and end_date."""
    if task.parent:
        update_task(task.parent.pk, state=task.state, result=task.result,
                start_date=task.start_date, end_date=task.end_date)


def is_launchable(node, process):
    completed = 0
    
    # All the successful parent tasks of the node
    parent_tasks = process.task_set.select_related().filter(state='SUCCESS')

    # For every parent transitions of the node
    for parent_transition in node.parent_transition_set.iterator():

        # If it has a successful task with his result met as parent
        if parent_tasks.filter(node=parent_transition.parent,  result__in=(
            '', parent_transition.condition)):

            # With XOR join only one parent has to be OK
            if node.join == 'XOR':
                return True
            else:
                completed += 1

    # With AND join all the parents has to be OK
    if node.join == 'AND' and\
            completed == node.parent_transition_set.count():
                return True


def get_pending_childs(task):
    """ Return the list of workflow nodes that must be launched when a task
    finishes. If task's node's split mode is XOR, only first found child node
    is returned."""
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
    parent_transitions = task.node.parent_transition_set.iterator()
    return task.process.task_set.filter(state='STARTED',
            node__child_transition_set__in=parent_transitions).annotate(
                    child_num=Count('node__child_transition_set')).filter(
                            child_num=1)


def get_alternative_way(task):
    """ Find another node in the workflow that can be started."""
    ways = [task.node]
    while ways:
        way = ways.pop()
        parent_transitions = way.parent_transition_set.filter(split='XOR')
        siblings = Node.objects.filter(parent_transition_set=parent_transitions)

        for sibling in siblings:
            if is_launchable(sibling, task.process):
                return sibling

        parents = Node.objects.filter(child_transition_set=parent_transitions)
        ways.append(parents)
    return None
