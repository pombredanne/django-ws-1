##################################################################################
#  Copyright 2011,2012 GISA Elkartea.                                            #
#                                                                                #
#  This file is part of django-ws.                                               #
#                                                                                #
#  django-ws is free software: you can redistribute it and/or modify it under    #
#  the terms of the GNU Affero General Public License as published by the Free   #
#  Software Foundation, either version 3 of the License, or (at your option)     #
#  any later version.                                                            #
#                                                                                #
#  django-ws is distributed in the hope that it will be useful, but WITHOUT ANY  #
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS     #
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for      #
#  more details.                                                                 #
#                                                                                #
#  You should have received a copy of the GNU Affero General Public License      #
#  along with django-ws. If not, see <http://www.gnu.org/licenses/>.             #
##################################################################################

from datetime import datetime

from celery.task import task
from celery.log import get_default_logger
from celery.contrib.abortable import AbortableAsyncResult
from celery.task.control import revoke

logger = get_default_logger()

from ws.models import Task, Node, Process, Transition
from ws.celery.shortcuts import (update_task, update_process, update_parent,
        get_pending_childs, get_revocable_parents, get_alternative_way)



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
    revoke(task_id, terminate=True)

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
