from django.contrib import admin
from ws.models import *

class TransitionAdmin(admin.ModelAdmin):
    list_display = ['parent', 'child', 'condition', 'workflow']
    list_filter = ['parent', 'child', 'workflow']

admin.site.register(Workflow)
admin.site.register(Node)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(Process)
admin.site.register(Task)
