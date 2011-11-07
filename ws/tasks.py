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
    form = AddForm
    def run(self, workflow_task, a, b):
        return a + b

class QueryForm(forms.BPMTaskForm):
    cuestion = forms.CharField(max_length=256,
                               label="Query")
    choices = forms.TextField(label="Choices")
    answer = forms.CharField(max_length=256,
                             label="Answer")

class query(BPMTask):
    form = QueryForm

    def run(self, workflow_task, cuestion, choices, answer):
        return answer
