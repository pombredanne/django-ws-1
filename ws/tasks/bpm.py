from ws.celery.tasks import BPMTask
from ws.celery import forms
from ws.models import Workflow, Process


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
