from datetime import datetime

from celery.task import task
from celery.task.sets import subtask
from celery.log import get_default_logger

logger = get_default_logger(name='event_dispatcher')

from ws.celery.events import dispatch
from ws.models import Task, Node, Process, Transition


@task(ignore_result=True, priority=1, mandatory=True)
def dispatcher():
    try:
        dispatch()
    except Exception, exc:
        dispatcher.retry(exc=exc)

@task(ignore_result=True)
def task_sent(task_pk, task_id):
    Task.objects.select_for_update().filter(pk=task_pk).update(
            task_id=task_id, state='SENT')


@task(ignore_result=True)
def task_received(task_id):
    Task.objects.select_for_update().filter(task_id=task_id).update(
            state='RECEIVED')


@task(ignore_result=True)
def task_started(task_id, timestamp):
    start_date = datetime.fromtimestamp(timestamp)
    Task.objects.select_for_update().filter(task_id=task_id).update(
            start_date=start_date, state='STARTED')


@task(ignore_result=True)
def task_succeeded(task_id, result, timestamp):
    task = Task.objects.select_for_update().filter(task_id=task_id)
    task.update(result=result, state='SUCCESS',
            end_date=datetime.fromtimestamp(timestamp))
    task = task[0]
    print task.process.task_set.filter(state='SUCCESS')

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


@task(ignore_result=True)
def task_failed(task_id, exception, traceback, timestamp):
    task = Task.objects.select_for_update().filter(task_id=task_id)
    task.update(state='FAILED', end_date=datetime.fromtimestamp(timestamp))
    task = task[0]

    xor = None
    while not xor:
        parents = task.node.parent_transition_set.filter(split='XOR')
        transitions = Transition.objects.filter(parent__in=parents,
                child__task_set__isnull=True)
        if transitions:
            xor = transitions[0]
    subtask('ws.celery.bpm.start').delay(
            node=xor.child, process=task.process)


@task(ignore_result=True)
def task_revoked(task_id):
    Task.objects.select_for_update().filter(task_id=task_id).update(
            state='REVOKED')


@task(ignore_result=True)
def task_retried(task_id):
    end_date = datetime.fromtimestamp(timestamp)
    Task.objects.select_for_update().filter(task_id=task_id).update(
            state='RETRIED', end_date=end_date)


@task(ignore_result=True)
def start(node, process):
    node = Node.objects.get(pk=node)
    process = Process.objects.get(pk=process)

    completed = 0
    tasks = process.task_set.select_related().filter(state='SUCCESS')
    print tasks
    for transition in node.parent_transition_set.iterator():
        if tasks.filter(node=transition.parent,  result__in=(
            '', transition.condition)):
            completed += 1

            if node.join == 'XOR':
                return process.start_node(node)

    if node.join == 'AND' and\
            completed == node.parent_transition_set.count():
                return process.start_node(transition.child)
