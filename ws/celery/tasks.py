from __future__ import absolute_import

from celery.task import Task
from celery.execute import send_task

from ws.celery.forms import BPMTaskForm

class BPMTask(Task):
    abstract = True
    form = BPMTaskForm

    def notify_progress(self, workflow_task, progress):
        send_task('ws.celery.bpm.task_progress', kwargs={
            'pk': workflow_task, 'progress': progress})

    def iter_progress(self, process):
        import pexpect
        while not process.terminated:
            try:
                process.expect('(\d{1,3})%')
            except pexpect.EOF:
                break
            progress = process.match.groups()[0]
            yield progress
