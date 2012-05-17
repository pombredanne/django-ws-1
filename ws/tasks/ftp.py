from django.utils.translation import ugettext as _

from ws import forms
from ws.tasks.http import _download

class DownloadForm(forms.BPMTaskForm):
    class Meta:
        title = _('download a file from a FTP server')
        description = _('')
    url = forms.CharField(max_length=500, label='url', initial='ftp://')


class download(_download):
    form = DownloadForm
