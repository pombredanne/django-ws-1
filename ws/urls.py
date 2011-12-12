from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from ws.views import (ProcessListView, WorkflowListView, TaskListView,
                      TaskFormView, TaskStartView, WorkflowGraphView,
                      CreateProcess, StartProcess, StopProcess)

urlpatterns = patterns('ws.views',
    (r'^$', TemplateView.as_view(template_name='ws/main.html')),
    #(r'^$', ProtectedTemplateView.as_view(template_name='ws/main.html')),
    (r'^login$', 'JSONLogin'),
    (r'^logout$', 'JSONLogout'),
    (r'^user.json$', 'UserInfoView'),

    (r'^workflows.json$', WorkflowListView.as_view()),
    #(r'^workflows/workflow_(?P<pk>.*).dot$', WorkflowGraphView.as_view()),
    #(r'^workflows/workflow_(?P<pk>.*).svg$', WorkflowGraphView.as_view()),
    (r'^workflows/workflow_(?P<pk>.*).png$', WorkflowGraphView.as_view()),
    (r'^processes.json$', ProcessListView.as_view()),
    (r'^process/new.json$', CreateProcess),
    (r'^process/start.json$', StartProcess),
    (r'^process/stop.json$', StopProcess),
    (r'^tasks.json$', TaskListView.as_view()),
    (r'^task/(?P<pk>.*)/form.json$', TaskFormView.as_view()),
    (r'^task/(?P<pk>.*)/start.json$', TaskStartView),
)
