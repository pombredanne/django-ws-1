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

"""Bindings for tying BPMTask events to callback celery tasks.

Functions:
    :func:`bpm_only`
        decorator for excluding tasks that don't inherit from ws.tasks.BPMTask

Classes:
    :func:`SignalResponses`
        bind BPMTasks to callback events
"""

from time import time
from functools import wraps

from celery.signals import task_prerun, task_postrun
from celery.datastructures import ExceptionInfo
from celery.utils.term import colored
from celery.log import get_default_logger

logger = get_default_logger()
c = colored()

from ws.tasks import BPMTask


def bpm_only(func):
    """Call a function only when it receives an object inherited from
    :class:`ws.tasks.BPMTask` as it's 'task' argument.
    """
    @wraps(func)
    def wrapper(self, task, *args, **kwargs):
        if isinstance(task, BPMTask):
            return func(self, task=task, *args, **kwargs)
    return wrapper


class SignalResponses(object):
    """Binding between celery BPMTask events and callback tasks.

    Methods:
        :meth:`connect`
            make the binding between events and tasks

    Attributes:
        :attr:`task_started`
            task called when a BPMTask starts
        :attr:`task_retried`
            task called when a BPMTask is retried
        :attr:`task_failed`
            task called when a BPMTask fails
        :attr:`task_succeeded`
            task called when a BPMTask is succeeded
    """

    def connect(self, task_started, task_retried, task_failed, task_succeeded):
        """Connect the celery BPMTask events to callback celery tasks."""
        self.task_started = task_started
        self.task_retried = task_retried
        self.task_failed = task_failed
        self.task_succeeded = task_succeeded
        task_prerun.connect(self._task_prerun)
        task_postrun.connect(self._task_postrun)

    @bpm_only
    def _task_prerun(self, task_id, task, args, kwargs, **kwds):
        """Call the task defined for when a BPMTask is started."""
        task.on_start(task_id, args, kwargs)

        if 'workflow_task' in kwargs:
            pk = kwargs['workflow_task']
        else:
            pk = args[0]

        if self.task_started is not None:
            self.task_started.apply_async(kwargs={
                'pk': pk, 'task_id': task_id})

        logger.debug('{state}: {task}'.format(
            state=c.bold('STARTED'), task=task))

    @bpm_only
    def _task_postrun(self, task_id, task, args, kwargs, retval, **kwds):
        """Distinguish between a failed, a retried and a succeeded BPMTask.
        Call the task defined for every of this events."""

        # If the returning value is an exception, it's not succeeded
        if isinstance(retval, ExceptionInfo):

            # Retry the task if it's possible to do so
            try:
                task.retry(exc=retval)
                if self.task_retried is not None:
                    self.task_retried.apply_async(kwargs={'task_id': task_id})

            # Mark the task failed if it's not
            except task.MaxRetriesExceededError:
                if self.task_failed is not None:
                    self.task_failed.apply_async(kwargs={'task_id': task_id})
        else:
            if self.task_succeeded is not None:
                self.task_succeeded.apply_async(kwargs={
                    'task_id': task_id, 'result': retval})
