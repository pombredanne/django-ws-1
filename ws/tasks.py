from ws.celery.tasks import BPMTask
from ws.celery import forms
from ws.models import Workflow, Process


class dummy(BPMTask):
    form = forms.BPMTaskForm
    def run(self, workflow_task):
        return ''


class endless(BPMTask):
    form = forms.BPMTaskForm
    def run(self, workflow_task):
        while True:
            pass


class AddForm(forms.BPMTaskForm):
    a = forms.IntegerField(label="First number",
                           initial=2,
                           help_text="Must be a integer number",
                           max_value=999,
                           min_value=0)
    b = forms.IntegerField(label="Second number",
                           initial=2,
                           help_text="Must be a integer number",
                           max_value=999,
                           min_value=0)

class add(BPMTask):
    form = AddForm
    def run(self, workflow_task, a, b):
        return a + b


class SubprocessForm(forms.BPMTaskForm):
    workflow = forms.ModelChoiceField(queryset=Workflow.objects.all(),
                                      label="Workflow",
                                      empty_label=None)
    name = forms.CharField(max_length=100,
                           label="Name")
    priority = forms.IntegerField(min_value=0, max_value=9, initial=9,
                                  label="Priority")

class subprocess(BPMTask):
    form = SubprocessForm

    def run(self, workflow_task, workflow, name, priority):
        self.process = Process.objects.create(workflow_id=workflow,
               name=name, priority=priority)
        self.process.start()
