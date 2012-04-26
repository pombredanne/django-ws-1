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

from django.contrib import admin
from ws.models import *


class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'workflow', 'join', 'split',
                    'task_name', 'params']
    list_filter = ['workflow', 'role']


class TransitionAdmin(admin.ModelAdmin):
    list_display = ['parent', 'child', 'condition', 'workflow']
    list_filter = ['parent', 'child', 'workflow']


class ProcessAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'workflow', 'start_date', 'end_date']
    list_filter = ['workflow']


admin.site.register(Workflow)
admin.site.register(Node, NodeAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(Process, ProcessAdmin)
admin.site.register(Task)
