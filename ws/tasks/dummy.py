from ws.celerytask import BPMTask
from ws import forms

class dummy(BPMTask):
    class Meta:
        name = 'Dummy'
        description = 'Silly dummy function'
    form = forms.BPMTaskForm
    def run(self, workflow_task):
        return ''
