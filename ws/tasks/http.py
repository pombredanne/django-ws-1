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

from tempfile import NamedTemporaryFile
from os import path
from urllib2 import urlopen
from math import floor
from shutil import copyfile

from django.conf import settings

from ws.tasks import BPMTask
from ws import forms


class DownloadForm(forms.BPMTaskForm):
    url = forms.CharField(max_length=500, label="Name")


class download(BPMTask):
    form = DownloadForm

    def run(self, workflow_task, url):
        destination = path.join(settings.MEDIA_ROOT, path.basename(url))
        temp = NamedTemporaryFile()

        request = urlopen(url)
        size = int(request.info().getheader('Content-Length').strip())
        downloaded = 0
        while True:
            chunk = request.read(1024**2) # 1MB chunks
            downloaded += len(chunk)
            progress = floor(downloaded / size * 100)
            self.notify_progress(workflow_task, progress)
            if not chunk:
                break
            temp.file.write(chunk)
        temp.file.close()
        copyfile(temp.name, destination)
        return destination
