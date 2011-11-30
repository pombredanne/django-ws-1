from datetime import datetime

from celery.task import task
from celery.task.sets import subtask

from ws.models import Task, Node, Process, Transition


@task
def task_sent(task_pk, task_id):
    Task.objects.filter(pk=task_pk).update(task_id=task_id, state='SENT')


@task
def task_received(task_id):
    Task.objects.filter(task_id=task_id).update(state='RECEIVED')


@task
def task_started(task_id, timestamp):
    start_date = datetime.fromtimestamp(timestamp)
    Task.objects.filter(task_id=task_id).update(
            start_date=start_date, state='STARTED')


@task
def task_succeeded(task_id, result, timestamp):
    task = Task.objects.get(task_id=task_id)
    task.result = result
    task.state = 'SUCCESS'
    task.end_date = datetime.fromtimestamp(timestamp)
    task.save()

    workflow = task.node.workflow
    if workflow.end == task.node:
        process = task.process
        process.end_date = datetime.now()
        process.save()
        
    transitions = task.node.child_transition_set.filter(
            condition__in=('', result))
    if task.node.split == 'XOR':
        transitions = transitions[:1]
    for transition in transitions.iterator():
        subtask('ws.celery.bpm.start').delay(
                node=transition.child.pk, process=task.process.pk)


@task
def task_failed(task_id, exception, traceback, timestamp):
    task = Task.objects.get(task_id=task_id)
    task.state = 'FAILED'
    task.end_date = datetime.fromtimestamp(timestamp)
    task.save()

    xor = None
    while not xor:
        parents = task.node.parent_transition_set.filter(split='XOR')
        transitions = Transition.objects.filter(parent__in=parents,
                child__task_set__isnull=True)
        if transitions:
            xor = transitions[0]
    subtask('ws.celery.bpm.start').delay(
            node=xor.child, process=task.process)


@task
def task_revoked(task_id):
    Task.objects.filter(task_id=task_id).update(state='REVOKED')


@task
def task_retried(task_id):
    end_date = datetime.fromtimestamp(timestamp)
    Task.objects.filter(task_id=task_id).update(
            state='RETRIED', end_date=end_date)


@task
def start(node, process):
    node = Node.objects.get(pk=node)
    process = Process.objects.get(pk=process)

    completed = 0
    tasks = process.task_set.filter(state='SUCCESS')
    for transition in node.parent_transition_set.iterator():
        if tasks.filter(node=transition.parent,  result__in=(
            '', transition.condition)):
            completed += 1

            if node.join == 'XOR':
                return process.start_node(node)

    if node.join == 'AND' and\
            completed == node.parent_transition_set.count():
                return process.start_node(transition.child)
