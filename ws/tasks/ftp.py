from ws import forms
from ws.tasks.http import _download

class DownloadForm(forms.BPMTaskForm):
    url = forms.CharField(max_length=500, label='url', initial='ftp://')


class download(_download):
    form = DownloadForm
