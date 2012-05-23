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

"""BPM logical tasks"""
__all__ = ['task_started', 'task_succeeded', 'task_failed', 'task_retried',
        'task_revoked', 'task_progress']

from django.utils.timezone import now
from celery.task import task
from celery.log import get_default_logger
from celery.contrib.abortable import AbortableAsyncResult
from celery.task.control import revoke

logger = get_default_logger()

from ws.celery.shortcuts import (update_task, update_process,
        get_pending_childs, get_revocable_parents, get_alternative_way)


@task(ignore_result=True)
def task_started(pk, task_id):
    """Mark the task as started and execute BPM logic:

        - if it's the beginning of a process, mark the process as started
        - if there is no need of them, cancel the running ancestors
    """
    task = update_task(pk=pk, task_id=task_id, state='STARTED', 
            start_date=now())

    if task.node.is_start:
        task.process.update(state='STARTED', start_date=task.start_date)
        logger.info('Process "{}" started'.format(task.process))

    for parent in task.get_revocable_parents():
        parent.revoke()
        logger.info('Parent task "{}" is not longer needed for task "{}"'.format(
            parent, task))


@task(ignore_result=True)
def task_succeeded(pk, result):
    """Mark the task as succeeded and execute BPM logic:

        - if it's the ending of a process, mark the process as suceeded
        - launch the needed children
    """
    task = update_task(pk=pk, state='SUCCESS', result=result,
            progress=100, end_date=now())

    if task.node.is_end:
        task.process.update(state='SUCCESS', end_date=task.end_date)
        logger.info('Process "{}" succeeded'.format(task.process))

    for child in task.get_pending_childs():
        task.process.launch_node(child)
        logger.info('Node "{child}" launched by task "{task}"'.format(
            child=child, task=task))


@task(ignore_result=True)
def task_failed(pk):
    """Mark the task as failed and execute BPM logic:

        - if it's the ending of a process, mark the process as failed
        - if there's an alternative way to continue the workflow,
          execute the alternative tasks
    """
    task = update_task(pk=pk, state='FAILED', end_date=now())

    if task.node.is_end:
        task.process.update(state='FAILED', end_date=task.end_date)
        logger.info('Process "{process}" failed'.format(process=task.process))

    task.get_alternative_way()
    if alternative:
        task.process.launch_node(alternative)
        logger.info('Alternative node "{alternative}" launched by task '
                '"{task}"'.format(alternative=alternative, task=task))


@task(ignore_result=True)
def task_revoked(pk):
    """Stop the task, mark it as revoked and execute BPM logic:

        - if the task executed a subprocess, revoke the process
    """
    task = update_task(pk=pk, state='REVOKED', end_date=now())

    result = AbortableAsyncResult(task.task_id)
    result.abort()
    revoke(task.task_id, terminate=True)

    for subprocess in task.subprocesses.iterator():
        subprocess.stop()
        subprocess.update(state='REVOKED', end_date=task.end_date)
        logger.info('Subprocess "{subprocess}" revoked by task '
                '"{task}"'.format(subprocess=subprocess, task=task))


@task(ignore_result=True)
def task_retried(pk):
    """Mark the task as retried."""
    update_task(pk, state='RETRIED')


@task(ignore_result=True)
def task_progress(pk, progress):
    """Update the tasks progress."""
    update_task(pk=pk, progress=progress)
