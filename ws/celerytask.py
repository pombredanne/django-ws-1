from celery.task import Task
from ws.models import Task as TaskModel
from ws.forms import BPMTaskForm

class BPMTask(Task):

    abstract = True

    form = BPMTaskForm

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        super(BPMTask, self).after_return(status, retval, task_id, args,
                                          kwargs, einfo)
        bpm_task = TaskModel.objects.get(pk = args[0])
        bpm_task.finish(status, retval)
