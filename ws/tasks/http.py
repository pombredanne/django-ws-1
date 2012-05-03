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


class DownloadForm(forms.BPMTaskForm):
    url = forms.CharField(max_length=500, label="Name")


class download(BPMTask):
    form = DownloadForm
    pass_workflow_task = True

    def call(self, workflow_task, url):
        wget = self.spawn('wget \'{url}\''.format(url=url))
        wget = self.track_task(wget, workflow_task)
        if wget.exitstatus != 0:
            raise Exception(str(wget))
