from django.utils.translation import ugettext as _

from ws.tasks import BPMTask
from ws import forms


class QuestionForm(forms.BPMTaskForm):
    title = forms.CharField(max_length=100, label=_('Title'))
    description = forms.CharField(max_length=1000, label=_('Description'),
            required=False)
    answer = forms.CharField(label=_('Answer'))

    @forms.with_cleaned_data
    def get_title(self):
        return self.cleaned_data['title']

    @forms.with_cleaned_data
    def get_description(self):
        return self.cleaned_data['description']


class question(BPMTask):
    form = QuestionForm

    def run(self, workflow_task, title, description, answer):
        return answer


class BooleanQuestionForm(QuestionForm):
    answer = forms.BooleanField(label=_('Answer'), required=False)


class boolean_question(BPMTask):
    form = BooleanQuestionForm

    def run(self, workflow_task, title, description, answer):
        return answer
