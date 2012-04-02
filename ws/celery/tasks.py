from __future__ import absolute_import
from time import sleep

from celery.task import Task
from celery.contrib.abortable import AbortableTask
from celery.execute import send_task
from pexpect import EOF

from ws.celery.forms import BPMTaskForm

class BPMTask(AbortableTask):
    abstract = True
    form = BPMTaskForm

    def notify_progress(self, workflow_task, progress):
        send_task('ws.celery.bpm.task_progress', kwargs={
            'pk': workflow_task, 'progress': progress})

    def iter_progress(self, process, every):
        while not process.terminated:
            try:
                process.expect('(\d{1,3})%')
            except EOF:
                break
            progress = process.match.groups()[0]
            yield progress
            sleep(every)

    def track_task(self, process, workflow_task, every=30):
        for progress in self.iter_progress(process, every):
            if self.is_aborted():
                return process
            else:
                self.notify_progress(workflow_task, progress)
