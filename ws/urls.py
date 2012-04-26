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
