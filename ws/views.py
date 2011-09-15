from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils import simplejson as json
from django.http import HttpResponse

from goflow.runtime.models import WorkItem
from goflow.workflow.models import Process

from ws.models import ProcessLauncher

class ProtectedTemplateView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedTemplateView, self).dispatch(*args, **kwargs)

class JSONResponseMixin(object):
    """ Inherit this before a generic view to send context in json format.
    """
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return HttpResponse(self.convert_context_to_json(context),
                            content_type='application/json')

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object.
        
        This function should be overriden with more specific code, this
        only works with integers and strings."""
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

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
    workitems = WorkItem.objects.list_safe(user=request.user, status=None,
                                           notstatus=None)
    data = {'success': True,
            'tasks':[]
    }
    for work in workitems:
        data['tasks'].append({
            'id': work.pk,
            'task': work.activity.title,
            'process': work.instance.title,
            'process_type': work.activity.process.title,
            'priority': work.priority,
            'date': work.date.strftime("%Y/%m/%d %H:%m"),
            'status': work.status
        })
    return HttpResponse(json.dumps(data),
                        mimetype="application/json")

class ProcessListView(JSONResponseMixin, ListView):
    model = Process

    def convert_context_to_json(self, context):
        data = {
            'success': True,
            'processes': [],
        }
        for process in context['process_list']:
            data['processes'].append({
                    'id': process.pk,
                    'title': process.title,
                    'description': process.description,
                    'enabled': process.enabled,
            })
        return json.dumps(data)

class ProcessLauncherListView(JSONResponseMixin, ListView):
    model = ProcessLauncher

    def convert_context_to_json(self, context):
        data = {
            'success': True,
            'processlaunchers': [],
        }
        for process in context['processlauncher_list']:
            data['processlaunchers'].append({
                    'id': process.pk,
                    'title': process.title,
            })
        return json.dumps(data)
