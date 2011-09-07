from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils import simplejson as json
from django.http import HttpResponse

class ProtectedTemplateView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedTemplateView, self).dispatch(*args, **kwargs)

def JSONLogin(request):
    success = False
    message = ""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            success = True
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
        else:
            message = 'Invalid form data.'
    else:
        message = 'login must be done with a POST request.'
    request.session.set_test_cookie()
    return HttpResponse(json.dumps({'success':success, 'message': message}),
                        mimetype="application/json")

@login_required
def TaskListView(request):
    data = {
        'success': True,
        'tasks': [
            {'id': 1, 'task': 'ordainketa egiaztatu', 'process': 'Futurama 1',           'process_type': 'kapitulu berri bat', 'priority': 5, 'date':'2011/08/31 10:05'},
            {'id': 2, 'task': 'gidoia idatzi',        'process': 'Futurama 1',           'process_type': 'kapitulu berri bat',  'priority': 3, 'date':'2011/08/31 10:05'},
            {'id': 3, 'task': 'komuna garbitu',       'process': 'lokalaren mantentzea', 'process_type': 'mantentzea',          'priority': 1, 'date':'2011/08/31 10:05'},
            {'id': 4, 'task': 'argazkiak aukeratu',   'process': '15M erreportaia',      'process_type': 'erreportai grafikoa', 'priority': 5, 'date':'2011/08/31 10:05'},
            {'id': 5, 'task': 'faktura bidali',       'process': 'Futurama 1',           'process_type': 'kapitulu berri bat',  'priority': 5, 'date':'2011/08/31 10:05'},
        ]
    }
    return HttpResponse(json.dumps(data),
                        mimetype="application/json")

