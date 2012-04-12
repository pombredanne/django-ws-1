from datetime import datetime

from celery.task import task
from celery.log import get_default_logger
from celery.contrib.abortable import AbortableAsyncResult

logger = get_default_logger()

from ws.celery.signals import SignalResponses
from ws.models import Task, Node, Process, Transition
from ws.shortcuts import (update_task, update_process, update_parent,
        get_pending_childs, get_revocable_parents, get_alternative_way)


SignalResponses.connect()


@task(ignore_result=True)
def task_started(pk, task_id):
    task = update_task(pk=pk, task_id=task_id, state='STARTED',
            start_date=datetime.now())

    if task.node.workflow.start == task.node:
        update_process(task.process.pk, state='STARTED',
                start_date=task.start_date)
        logger.info('Process "{process}" started'.format(process=task.process))
        update_parent(task.process)

    for parent in get_revocable_parents(task):
        parent.revoke()
        logger.info('Parent task "{parent}" is not longer needed for task "{task}"'.format(
            parent=parent, task=task))


@task(ignore_result=True)
def task_succeeded(task_id, result):
    task = update_task(task_id=task_id, state='SUCCESS', progress=100,
            end_date=datetime.now())

    if task.node.workflow.end == task.node:
        update_process(task.process.pk, state='SUCCESS',
                end_date=task.end_date)
        logger.info('Process "{process}" succeeded'.format(process=task.process))
        update_parent(task.process)

    for child in get_pending_childs(task):
        task.process.launch_node(child)
        logger.info('Node "{child}" launched by task "{task}"'.format(
            child=child, task=task))


@task(ignore_result=True)
def task_failed(task_id):
    task = update_task(task_id=task_id, state='FAILED',
            end_date=datetime.now())

    if task.node.workflow.end == task.node:
        update_process(task.process.pk, state='FAILED',
                end_date=task.end_date)
        logger.info('Process "{process}" failed'.format(process=task.process))
        update_parent(task_process)

    alternative = get_alternative_way(task)
    if alternative:
        task.process.launch_node(alternative)
        logger.info('Alternative node "{alternative}" launched by task "{task}"'.format(
            alternative=alternative, task=task))


@task(ignore_result=True)
def task_revoked(task_id):
    result = AbortableAsyncResult(task_id)
    result.abort()
    result.revoke()
    #revoke(task_id, terminate=True)

    task = update_task(task_id=task_id, state='REVOKED', end_date=datetime.now())
    try:
        subprocess = Process.objects.get(parent=task)
    except Process.DoesNotExist:
        pass
    else:
        subprocess.stop()
        update_process(subprocess.pk, state='REVOKED',
                end_date=task.end_date)
        logger.info('Subprocess "{subprocess}" revoked by task "{task}"'.format(
            subprocess=subprocess, task=task))


@task(ignore_result=True)
def task_retried(task_id):
    update_task(task_id=task_id, state='RETRIED')

@task(ignore_result=True)
def task_progress(pk, progress):
    update_task(pk=pk, progress=progress)
