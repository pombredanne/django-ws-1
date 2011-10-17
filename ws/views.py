from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
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

class ExtListView(JSONResponseMixin, ListView):
    """
    List view prepared to send data to a ExtJS application.
    Features:

        - send response in JSON format
        - look for pagination parameters
        - send 'success' value
        - send listings inside a 'rows' array.

    The convert_object_to_json function should be overwritten to provide
    specific information for each row.
    """
    def get_paginate_by(self, queryset):
        limit = self.request.GET.get('limit', self.paginate_by)
        try:
            limit = int(limit)
        except ValueError:
            limit = None
        return limit

    def convert_context_to_json(self, context):
        if context['paginator'] is not None:
            total = context['paginator'].count
        else:
            total = len(context['object_list'])
        data = {'success': True,
                'total': total,
                'rows':[]
        }
        for obj in context['object_list']:
            data['rows'].append(self.convert_object_to_dict(obj))
        return json.dumps(data)

    def convert_object_to_dict(obj):
        """ Convert a object to a dict, with keys as strings, and values
        serializable to JSON."""
        return {
            'pk': obj.pk,
            'name': unicode(obj),
        }

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

def JSONLogout(request):
    logout(request)
    return HttpResponse(json.dumps({'success':True, 'message': 'Logged out'}),
                        mimetype="application/json")

class TaskListView(ExtListView):
    model = WorkItem

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskListView, self).dispatch(*args, **kwargs)

    def convert_object_to_dict(self, obj):
        if obj.user:
            user = obj.user.username
        else:
            user = "unknown"
        data = {
            'id': obj.pk,
            'task': obj.activity.title,
            'user': user,
            'process': obj.instance.title,
            'process_type': obj.activity.process.title,
            'priority': obj.priority,
            'date': obj.date.strftime("%Y/%m/%d %H:%m"),
            'status': obj.status
        }
        return data

class ProcessListView(ExtListView):
    model = Process

    def convert_object_to_dict(self, obj):
        data = {
            'id': obj.pk,
            'title': obj.title,
            'description': obj.description,
            'enabled': obj.enabled,
        }
        return data

class ProcessLauncherListView(ExtListView):
    model = ProcessLauncher

    def convert_object_to_dict(self, obj):
        data = {
            'id': obj.pk,
            'title': obj.title,
        }
        return data

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

class RunningProcessListView(ExtListView):
    model = ProcessInstance

    def convert_object_to_dict(self, obj):
        data = {
            'id': obj.pk,
            'title': obj.title,
            'type': obj.process.title,
            'creationTime': obj.creationTime.strftime("%Y/%m/%d %H:%m"),
            'status': obj.status,
        }
        return data

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
