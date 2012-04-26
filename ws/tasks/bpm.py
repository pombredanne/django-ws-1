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

from ws.tasks import BPMTask
from ws import forms
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
