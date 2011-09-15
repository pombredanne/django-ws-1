from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from ws.views import ProcessListView, ProcessLauncherListView

urlpatterns = patterns('ws.views',
    (r'^$', TemplateView.as_view(template_name='ws/main.html')),
    #(r'^$', ProtectedTemplateView.as_view(template_name='ws/main.html')),
    (r'^login$', 'JSONLogin'),
    (r'^tasks.json$', 'TaskListView'),
    (r'^processes.json$', ProcessListView.as_view()),
    (r'^processlaunchers.json$', ProcessLauncherListView.as_view()),
)
