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

from django.utils.translation import ugettext as _

from ws.tasks import BPMTask
from ws import forms


class QuestionForm(forms.BPMTaskForm):
    class Meta:
        title = _('ask a question to a human')
        description = ''
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
    class Meta:
        title = _('ask a true/false question to a human')
        description = ''
    answer = forms.BooleanField(label=_('Answer'), required=False)


class boolean_question(BPMTask):
    form = BooleanQuestionForm

    def run(self, workflow_task, title, description, answer):
        return answer
