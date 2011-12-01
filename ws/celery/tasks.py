from __future__ import absolute_import

from celery.task import Task

from ws.celery.forms import BPMTaskForm

class BPMTask(Task):
    abstract = True
    form = BPMTaskForm
