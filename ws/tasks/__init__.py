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

"""Celery tasks on steroids.

Submodules:
    Automatically detected and imported.

Classes:
    :class:`BPMTask`
        intended for inheritance by celery tasks

Functions:
    :func:`load_task_submodules`
        automatically load all submodules
"""

from time import sleep

from celery.contrib.abortable import AbortableTask
from celery.execute import send_task
from pexpect import spawn, EOF

from ws.forms import BPMTaskForm


class BPMTask(AbortableTask):
    """Abstract class intended for inheritance by celery tasks.

    Functions:
        :meth:`run`
         wrapper around call method
        :meth:`spawn`
         spawn a subprocess
        :meth:`notify_progress`
         execute task for updating the progress of a task
        :meth:`iter_progress`
         iterate over the progress of a task
        :meth:`track_task`
         track the progress of a task
        :meth:`call`
         actual task
        :meth:`on_start`
         executed when a task starts
        :meth:`on_success`
         executed when a task is succeeded
        :meth:`on_failure`
         executed when a task fails
        :meth:`on_retry`
         executed when a task is retried
        :meth:`on_revoke`
            executed when a task is revoked

    Attributes:
        :attr:`form`
            related form
    """
    abstract = True
    form = BPMTaskForm

    def run(self, workflow_task, *args, **kwargs):
        return self.call(*args, **kwargs)

    def spawn(self, process):
        """Spawn a subprocess."""
        return spawn(process)

    def notify_progress(self, workflow_task, progress):
        """Execute task for updating the progress of a task."""
        send_task('ws.celery.bpm.task_progress', kwargs={
            'pk': workflow_task, 'progress': progress})

    def iter_progress(self, process, every, regexp='(\d{1,3})%'):
        """Iterate over the progress of a task.

        Keyword arguments:
            process     
                process returned by BPMTask.spawn
            every
                interval in seconds for iteration
            regexp
                progress regexp
        """
        while not process.terminated:
            try:
                process.expect(regexp)
            except EOF:
                break
            progress = process.match.groups()[0]
            yield progress
            sleep(every)

    def track_task(self, process, workflow_task, every=30):
        """Iterate over the progress of a task and update his state.

        Keyword arguments:
            process
                process returned by BPMTask.spawn
            workflow_task
                django's id for a ws.models.Task
            every
                interval in seconds for updating
        """
        for progress in self.iter_progress(process, every):
            if self.is_aborted():
                return process
            else:
                self.notify_progress(workflow_task, progress)

    def call(self, *args, **kwargs):
        pass

    def on_start(self, task_id, args, kwargs):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_revoke(self, task_id, args, kwargs):
        pass


def load_task_submodules(module_name):
    """Load submodules of module so that tasks are automatically detected by celery."""
    import os
    from celery.loaders.default import Loader
    loader = Loader()
    module = loader.import_task_module(module_name)
    directory = os.path.dirname(module.__file__)
    for filename in os.listdir(directory):
        filename, extension = os.path.splitext(filename)
        if extension == '.py':
            yield loader.import_task_module('{}.{}'.format(module_name, filename))
load_task_submodules('ws.tasks')
