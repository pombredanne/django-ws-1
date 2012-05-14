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

"""
WS's Celery tasks. All use :class:`ws.tasks.BPMTask` as base class.
"""

from time import sleep
from inspect import getargspec

from django import forms

from celery.registry import tasks as task_registry
from celery.contrib.abortable import AbortableTask
from celery.execute import send_task
from pexpect import spawn, EOF

from ws.forms import BPMTaskForm


class BPMTask(AbortableTask):
    """Abstract class intended for inheritance by celery tasks.

    Attributes:
        :attr:`form`
            related :class:`ws.forms.BPMTaskForm`
    """
    abstract = True
    form = BPMTaskForm

    @classmethod
    def _filter_params(klass, params):
        # If there's a related form with some fields, cleanup params with it
        if klass.form is not None and klass.form.base_fields.keys():
            form = klass.form(params)
            if form.is_valid():
                kwargs = form.clean()
            else:
                raise forms.ValidationError('Invalid or insufficient parameters')

        # Else, inspect the tasks run method
        else:
            args = getargspec(klass.run)
            
            # If it accepts no *args nor **kwargs, pass only the accepted args
            if (args.varargs, args.keywords) == (None, None):

                # don't pass workflow_task, as it's passed automatically later
                kwargs = { arg: params[arg] for arg in args.args if arg not
                          in ('self', 'workflow_task') }

            # Else, pass them all
            else:
                kwargs = params

            # Args without default values
            args = args.args[:-len(args.defaults or ())]

            # Assert that all needed args are given
            if not all([arg in kwargs for arg in args]):
                raise forms.ValidationError('Insufficient parameters')

        return kwargs

    @classmethod
    def _info_required(klass, params):
        try:
            klass._filter_params(params)
        except forms.ValidationError:
            return True
        else:
            return False

    def run(self, workflow_task, *args, **kwargs):
        """ actual task, must receive 'workflow_task' argument """
        raise NotImplemented

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

    def on_start(self, task_id, args, kwargs):
        """ executed when a task starts """
        pass

    def on_success(self, retval, task_id, args, kwargs):
        """ executed when a task is succeeded """
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """ executed when a task fails """
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """ executed when a task is retried """
        pass

    def on_revoke(self, task_id, args, kwargs):
        """ executed when a task is revoked """
        pass


def get_registered_tasks():
    from celery.loaders import current_loader
    from ws.tasks import BPMTask
    current_loader = current_loader()
    current_loader.import_default_modules()
    return [key for key, value in task_registry.items()\
            if isinstance(value, BPMTask)]
