from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from ws.views import (ProcessListView, ProcessLauncherListView,
                      ProcessLauncherDetailView, RunningProcessListView,
                      TaskListView)

urlpatterns = patterns('ws.views',
    (r'^$', TemplateView.as_view(template_name='ws/main.html')),
    #(r'^$', ProtectedTemplateView.as_view(template_name='ws/main.html')),
    (r'^login$', 'JSONLogin'),
    (r'^logout$', 'JSONLogout'),
    (r'^tasks.json$', TaskListView.as_view()),
    (r'^processes.json$', ProcessListView.as_view()),
    (r'^runningprocesses.json$', RunningProcessListView.as_view()),
    (r'^processlaunchers.json$', ProcessLauncherListView.as_view()),
    (r'^processlauncher/(?P<pk>\d+).json$', ProcessLauncherDetailView.as_view()),
    (r'^startprocess.json$', 'StartProcessView'),
)
