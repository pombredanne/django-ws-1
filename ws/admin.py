from django.contrib import admin
from ws.models import *

admin.site.register(Workflow)
admin.site.register(Node)
admin.site.register(Transition)
admin.site.register(Process)
admin.site.register(Task)
