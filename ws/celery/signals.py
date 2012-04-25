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

from time import time

from celery.signals import task_sent, task_prerun, task_postrun, task_failure
from celery.datastructures import ExceptionInfo
from celery.execute import send_task
from celery.utils.term import colored
from celery.log import get_default_logger

logger = get_default_logger()
c = colored()

from ws.celery.tasks import BPMTask


def bpm_only(func):
    def wrapper(task, *args, **kwargs):
        if isinstance(task, BPMTask):
            return func(task=task, *args, **kwargs)
    return wrapper


class SignalResponses(object):
    task_started = None
    task_retried = None
    task_failed = None
    task_succeeded = None

    @staticmethod
    def connect():
        task_prerun.connect(SignalResponses.task_prerun)
        task_postrun.connect(SignalResponses.task_postrun)

    @staticmethod
    @bpm_only
    def task_prerun(task_id, task, args, kwargs, **kwds):
        task.on_start(task_id, args, kwargs)

        if kwargs.has_key('workflow_task'):
            pk = kwargs['workflow_task']
        else:
            pk = args[0]

        if self.task_started is not None:
            self.task_started.apply_async(kwargs={'pk': pk, 'task_id': task_id})

        logger.debug('{state}: {task}'.format(
            state=c.bold('STARTED'), task=task))

    @staticmethod
    @bpm_only
    def task_postrun(task_id, task, args, kwargs, retval, **kwds):
        if isinstance(retval, ExceptionInfo):
            try:
                task.retry(exc=retval)
                if self.task_retried is not None:
                    self.task_retried.apply_async(kwargs={'task_id': task_id})
            except task.MaxRetriesExceededError:
                if self.task_failed is not None:
                    self.task_failed.apply_async(kwargs={'task_id': task_id})
        else:
            if self.task_succeeded is not None:
                self.task_succeeded.apply_async(kwargs={
                    'task_id': task_id, 'result': retval})
