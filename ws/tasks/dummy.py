##################################################################################
#  Copyright 2011,2012 GISA Elkartea.                                            #
#                                                                                #
#  This file is part of django-ws.                                               #
#                                                                                #
#  django-ws is free software: you can redistribute it and/or modify it under    #
#  the terms of the GNU Affero General Public License as published by the Free   #
#  Software Foundation, either version 3 of the License, or (at your option)     #
#  any later version.                                                            #
#                                                                                #
#  django-ws is distributed in the hope that it will be useful, but WITHOUT ANY  #
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS     #
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for      #
#  more details.                                                                 #
#                                                                                #
#  You should have received a copy of the GNU Affero General Public License      #
#  along with django-ws. If not, see <http://www.gnu.org/licenses/>.             #
##################################################################################

from ws.celery.tasks import BPMTask
from ws.celery import forms
from time import sleep


class dummy(BPMTask):
    form = forms.BPMTaskForm
    def run(self, workflow_task):
        return ''


class endless(BPMTask):
    form = forms.BPMTaskForm
    def run(self, workflow_task):
        while True:
            sleep(1000)


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
