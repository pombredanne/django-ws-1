from django.db.models import Count
from ws.models import Task, Process


def update_process(pk, **kwargs):
    process_q = Process.objects.select_for_update().filter(pk=pk)
    process_q.update(**kwargs)
    return process_q[0]


def update_task(pk_or_task_id, **kwargs):
    try:
        task_q = Task.objects.select_for_update().filter(pk=pk_or_task_id)
    except ValueError:
        task_q = Task.objects.select_for_update().filter(task_id=pk_or_task_id)
    task_q.select_for_update().update(**kwargs)
    if task_q:
        return task_q[0]
    return None


def update_parent(task):
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
