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
"""
WS views, mostly JSON API for ExtJS.
"""

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import simplejson as json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from guardian.decorators import permission_required
from guardian.shortcuts import get_objects_for_user

from ws.models import Task, Process, Workflow, Transition


class ProtectedTemplateView(TemplateView):
    """ Generic template view, users must be logged in. """
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


class LoginRequiredMixin(object):
    """ Views that inherit this mixin had login required. """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ExtListView(LoginRequiredMixin, JSONResponseMixin, ListView):
    """
    List view prepared to send data to a ExtJS application.
    Features:

        - send response in JSON format
        - look for pagination parameters
        - send 'success' value
        - send listings inside a 'rows' array.

    The convert_object_to_dict function should be overwritten to provide
    specific information for each row.
    """

    #Default pagination
    paginate_by = 20

    def get_paginate_by(self, queryset):
        limit = self.request.GET.get('limit', self.paginate_by)
        try:
            limit = int(limit)
        except ValueError:
            limit = None
        return limit

    def get_queryset(self):
        query = super(ExtListView, self).get_queryset()

        ext_filters = self.request.GET.get('filter', None)
        if ext_filters:
            for ext_filter in json.loads(ext_filters):
                params = {ext_filter['property']: ext_filter['value']}
                query = query.filter(**params)
        return query

    def convert_context_to_json(self, context):
        if context['paginator'] is not None:
            total = context['paginator'].count
        else:
            total = len(context['object_list'])
        data = {'success': True,
                'total': total,
                'rows': [],
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
    """ Log in users with a JSON POST request.

        The request must give username and password fields.
    """
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
    return HttpResponse(json.dumps({'success': success, 'message': message}),
                        mimetype="application/json")


def JSONLogout(request):
    """ Log out current logged in user """
    logout(request)
    return HttpResponse(json.dumps({'success': True, 'message': 'Logged out'}),
                        mimetype="application/json")


class WorkflowListView(ExtListView):
    """ List of all workflows for a ExtJS store. """
    model = Workflow

    def convert_object_to_dict(self, obj):
        data = {
            'pk': obj.pk,
            'name': obj.name,
            #'description': obj.description,
            #'enabled': obj.enabled,
        }
        return data


class ProcessListView(ExtListView):
    """ List of all processes for a ExtJS store. """
    model = Process

    def convert_object_to_dict(self, obj):
        if obj.start_date:
            start_date = obj.start_date.strftime("%Y/%m/%d %H:%M")
        else:
            start_date = None
        if obj.end_date:
            end_date = obj.end_date.strftime("%Y/%m/%d %H:%M")
        else:
            end_date = None
        data = {
            'pk': obj.pk,
            'name': unicode(obj),
            'workflow': obj.workflow.name,
            'workflow_pk': obj.workflow.pk,
            'start_date': start_date,
            'end_date': end_date,
            'status': obj.state,
            #'creationTime': obj.creationTime.strftime("%Y/%m/%d %H:%M"),
        }
        return data


@permission_required('ws.execute_process')
def CreateProcess(request):
    """ Create a new process with a JSON POST request.

        Request params:
        
        workflow
            pk of the process's workflow.
        autostart
            'on' or 'off', to start process automatically after creation.
    """
    success = False
    message = ""
    if request.method == 'POST':
        workflow_id = request.POST.get('workflow', None)
        autostart = request.POST.get('autostart', 'off')
        if workflow_id is None:
            message = 'Workflow id required'
        else:
            name = request.POST.get('name', None)
            process = Process(workflow_id=workflow_id, name=name)
            try:
                process.save()
                success = True
                message = "Process created"
            except:
                message = 'Invalid workflow_id'
            if autostart == 'on':
                try:
                    process.start()
                    message = "Process created and started"
                except:
                    success = False
                    message = "Process created, but auto start failed"
    else:
        message = 'Data must be send in a POST request'

    return HttpResponse(json.dumps({'success': success,
                                    'message': message}),
                        mimetype="application/json")


@permission_required('ws.execute_process')
def StartProcess(request):
    """ Start a process with a JSON POST request.

        Request params:
        
        pk
            pk of the process
    """
    success = False
    message = ""
    if request.method == 'POST':
        process_pk = request.POST.get('pk', None)
        if process_pk is None:
            message = 'Process pk required'
        else:
            process = get_object_or_404(Process, pk=process_pk)
            try:
                process.start()
                success = True
                message = 'Process started'
            except AssertionError as error:
                message = error.args and error.args[0] or 'Unknown error'
                message = 'Unable to start process: ' + message
    else:
        message = 'Data must be send in a POST request'

    return HttpResponse(json.dumps({'success': success,
                                    'message': message}),
                        mimetype="application/json")


@permission_required('ws.execute_process')
def StopProcess(request):
    """ Stop a process with a JSON POST request.

        Request params:
        
        pk
            pk of the process
    """
    success = False
    message = ""
    if request.method == 'POST':
        process_pk = request.POST.get('pk', None)
        if process_pk is None:
            message = 'Process pk required'
        else:
            process = get_object_or_404(Process, pk=process_pk)
            try:
                process.stop()
                success = True
                message = 'Process stopped'
            except AssertionError as error:
                message = error.args and error.args[0] or 'Unknown error'
                message = 'Unable to stop process: ' + message
    else:
        message = 'Data must be send in a POST request'

    return HttpResponse(json.dumps({'success': success,
                                    'message': message}),
                        mimetype="application/json")


class TaskListView(ExtListView):
    """ List of tasks for a ExtJS store. Only tasks where the user has view
    permission.
    """
    model = Task

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset()
        return get_objects_for_user(self.request.user,
                'ws.view_task', queryset)

    def convert_object_to_dict(self, obj):
        #if obj.user:
        #    user = obj.user.username
        #else:
        #    user = "unknown"
        data = {
            'pk': obj.pk,
            'task': obj.node.name,
            'user': obj.user.username,
            'user_pk': obj.user.pk,
            'process': unicode(obj.process),
            'process_pk': obj.process.pk,
            'workflow': obj.process.workflow.name,
            'workflow_pk': obj.process.workflow.pk,
            #'priority': obj.priority,
            #'date': obj.date.strftime("%Y/%m/%d %H:%m"),
            'state': obj.state,
            'result': obj.result,
            'info_required': obj.node.info_required,
        }
        return data


class WorkflowGraphView(DetailView):
    """ Display a graph of nodes and transitions for a workflow. """
    model = Workflow

    def render_to_response(self, context):
        import pygraphviz as pgv
        import tempfile
        import os
        import random
        graph = pgv.AGraph(strict=False, directed=True)
        nodes = context['workflow'].node_set.all()
        role_colors = {}
        for node in nodes:
            if not node.role.name in role_colors:
                role_colors[node.role.name] = "#%s%s%s" % tuple(
                        [random.choice('1234567890abcdef') * 2\
                                for x in range(3)])
            graph.add_node(node, color=role_colors[node.role.name])
        for role, color in role_colors.items():
            graph.add_node(role, color=color, shape='note')
        for transition in Transition.objects.filter(parent__in=nodes):
            if transition.condition:
                label = str("[%s]" % transition.condition)
            else:
                label = ''
            graph.add_edge(transition.parent, transition.child,
                           label=label,
                           #headlabel=str(transition.parent.split),
                           taillabel=str(transition.parent.split),
                           headlabel=str(transition.child.join),
                           labelfontsize='8')
        #return HttpResponse(graph.string()) # .dot file
        png_file = tempfile.NamedTemporaryFile(delete=False)
        png_file_name = png_file.name
        graph.layout()
        #layout: [neato|dot|twopi|circo|fdp|nop]
        #graph.draw(png_file, format='svg', prog='dot')
        #graph.draw(png_file, format='svg', prog='circo')
        graph.draw(png_file, format='png', prog='dot')
        png_file = open(png_file_name)
        image = png_file.read()
        png_file.close()
        os.remove(png_file_name)
        return HttpResponse(image,
                            content_type='image/png')
                            #content_type='image/svg+xml')


class TaskFormView(DetailView):
    """ Return the fields required by the task as a ExtJS form items."""
    model = Task

    def render_to_response(self, context):
        form = context['task'].node.celery_task.obj.form()
        params = context['task'].node.params
        fields = form.get_fields(params)
        return HttpResponse(json.dumps(fields),
                            mimetype="application/json")


@permission_required('ws.execute_task', (Task, 'pk', 'pk'))
def TaskStartView(request, pk):
    """ Start a task and return success information in a JSON dict. """
    task = get_object_or_404(Task, pk=pk)
    # FIXME: Convert QueryDict to dict.  This could result in data lost if
    # some param is a "select multiple", but this should never happen.
    extra_params = dict(request.POST.items())
    try:
        result = task.launch(extra_params)
    except ValidationError:
        success = False
    else:
        success = True
    return HttpResponse(json.dumps({"success": success}),
                        mimetype="application/json")


def UserInfoView(request):
    """ Return information about currently logged user in a JSON response.

        Returns a dict:

        success
            true or false. True indicates a successfull request.

        username
            username of the current user

        pk
            pk of the current user
    """
    if request.user.is_authenticated():
        data = {'success': True,
                'username': request.user.username,
                'pk': request.user.pk}
    else:
        data = {'success': False}
    return HttpResponse(json.dumps(data),
                        mimetype='application/json')

"""
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
"""
