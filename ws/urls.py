from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from ws.views import (ProcessListView, WorkflowListView,
                      TaskListView)

urlpatterns = patterns('ws.views',
    (r'^$', TemplateView.as_view(template_name='ws/main.html')),
    #(r'^$', ProtectedTemplateView.as_view(template_name='ws/main.html')),
    (r'^login$', 'JSONLogin'),
    (r'^logout$', 'JSONLogout'),

    (r'^workflows.json$', WorkflowListView.as_view()),
    (r'^processes.json$', ProcessListView.as_view()),
    (r'^tasks.json$', TaskListView.as_view()),
)
