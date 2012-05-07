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

from django.core.mail import send_mail
from django.conf import settings
from ws.tasks import BPMTask
from ws import forms


class SendEmailForm(forms.BPMTaskForm):
    subject = forms.CharField(max_length=100, label='Subject')
    from_email = forms.CharField(max_length=100, label='From',
            initial=settings.DEFAULT_FROM_EMAIL)
    to = forms.CharField(max_length=2000, label='To',
            widget=forms.Textarea, )#help='Separate recipients with newlines')
    body = forms.CharField(max_length=5000, label='Body',
            widget=forms.Textarea)


class send_email(BPMTask):
    form = SendEmailForm

    def run(self, workflow_task, subject, from_email, to, body):
        to = [rcv.strip() for rcv in to.splitlines()]
        subject = '{} {}'.format(settings.EMAIL_SUBJECT_PREFIX, subject)
        send_email(subject, body, from_email, to)
