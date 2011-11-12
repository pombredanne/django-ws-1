from ws.celerytask import BPMTask
from ws import forms

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
    class Meta:
        name = 'Add'
        description = 'Add to integers'
    form = AddForm
    def run(self, workflow_task, a, b):
        return a + b
