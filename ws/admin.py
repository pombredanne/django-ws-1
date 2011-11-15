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
