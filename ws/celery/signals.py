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
    @staticmethod
    def connect():
        task_prerun.connect(SignalResponses.task_prerun)
        task_postrun.connect(SignalResponses.task_postrun)

    @staticmethod
    @bpm_only
    def task_prerun(task_id, task, args, kwargs, **kwds):
        if kwargs.has_key('workflow_task'):
            pk = kwargs['workflow_task']
        else:
            pk = args[0]

        send_task('ws.celery.bpm.task_started', kwargs={
            'pk': pk, 'task_id': task_id})

        logger.debug('{state}: {task}'.format(
            state=c.bold('STARTED'), task=task))

    @staticmethod
    @bpm_only
    def task_postrun(task_id, task, args, kwargs, retval, **kwds):
        if isinstance(retval, ExceptionInfo):
            try:
                task.retry(retval)
                send_task('ws.celery.bpm.task_retried', kwargs={
                    'task_id': task_id})
            except task.MaxRetriesExceededError:
                send_task('ws.celery.bpm.task_failed', kwargs={
                    'task_id': task_id})
        else:
            send_task('ws.celery.bpm.task_succeeded', kwargs={
                'task_id': task_id, 'result': retval})
