from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils import simplejson as json
from django.http import HttpResponse

from goflow.runtime.models import WorkItem, ProcessInstance
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

#page=1&start=0&limit=25
class TaskListView(JSONResponseMixin, ListView):
    model = WorkItem

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskListView, self).dispatch(*args, **kwargs)

    def convert_context_to_json(self, context):
        data = {'success': True,
                'tasks':[]
        }
        for work in context['workitem_list']:
            if work.user:
                user = work.user.username
            else:
                user = "unknown"
            data['tasks'].append({
                'id': work.pk,
                'task': work.activity.title,
                'user': user,
                'process': work.instance.title,
                'process_type': work.activity.process.title,
                'priority': work.priority,
                'date': work.date.strftime("%Y/%m/%d %H:%m"),
                'status': work.status
            })
        return json.dumps(data)

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

class ProcessLauncherDetailView(JSONResponseMixin, DetailView):
    model = ProcessLauncher

    def convert_context_to_json(self, context):
        model = context['processlauncher'].content_type.model_class()
        #FIXME?: maybe a class method should be better: model.ext_fields()
        fields = model().ext_fields()
        data = {
            'success': True,
            'fields': fields
        }
        return json.dumps(data)

class RunningProcessListView(JSONResponseMixin, ListView):
    model = ProcessInstance
    def convert_context_to_json(self, context):
        data = {
            'success': True,
            'runningprocesses': [],
        }
        for process in context['processinstance_list']:
            data['runningprocesses'].append({
                    'id': process.pk,
                    'title': process.title,
                    'type': process.process.title,
                    'creationTime': process.creationTime.strftime("%Y/%m/%d %H:%m"),
                    'status': process.status,
            })
        return json.dumps(data)

def StartProcessView(request):
    response = {}
    processlauncher_id = request.POST.get('process', None)
    response['success'] = True
    if processlauncher_id is None:
        response['success'] = False
    else:
        pl = ProcessLauncher.objects.get(pk=processlauncher_id)
        process_model = pl.content_type.model_class()
        class Form(ModelForm):
            class Meta:
                model = process_model
        form = Form(request.POST)
        item = None
        try:
            item = form.save()
        except ValueError:
            response['success'] = False
            return json.dumps(response)
        # The content is ready, let's start the process
        ProcessInstance.objects.start(
            process_name=pl.workflow.title,
            user=request.user,
            item=item
        )
    return HttpResponse(json.dumps(response),
                        mimetype="application/json")
