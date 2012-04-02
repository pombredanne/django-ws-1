from ws.celery.tasks import BPMTask
from ws.celery import forms

class DownloadForm(forms.BPMTaskForm):
    url = forms.CharField(max_length=500, label="Name")

class download(BPMTask):
    form = DownloadForm

    def run(self, workflow_task, url):
        from pexpect import spawn
        wget = spawn('wget \'{url}\''.format(url=url))
        wget = self.track_task(wget, workflow_task)
        if wget.exitstatus != 0:
            raise Exception(str(wget))
