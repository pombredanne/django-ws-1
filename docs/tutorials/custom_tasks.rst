===================
Custom celery tasks
===================


For creating your custom task, it's needed to add the module that contains the custom task to the 'CELERY_IMPORT' setting, inherit from BPMTask, and write a custom call method::

    from ws.tasks import BPMTask
    
    class MultiplyTask(BPMTask):

        def call(self, a, b):
            return a * b


If you want to use the ExtJS interface to give execution parameters to the task, you must setup a related form::

    from ws.tasks import BPMTask
    from ws import forms

    class MultiplyTaskForm(forms.BPMTaskForm):
        a = forms.IntegerField()
        b = forms.IntegerField()


    class MultiplyTask(BPMTask):
        form = MultiplyTaskForm
        
        def call(self, a, b):
            return a * b


It's also posible to define certain actions that will take place when certain events happen::

    from ws.tasks import BPMTask

    class MultiplyTask(BPMTask):
        
        def call(self, a, b):
            return a * b

        def on_start(self, task_id, args, kwargs):
            print('Task ID: {}'.format(task_id))
            print('Received args: {}'.format(args))
            print('Received kwargs: {}'.format(kwargs))

        def on_success(self, retval, task_id, args, kwargs):
            print('Return value: {}'.format(retval))

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            print('Exception: {}'.format(exc))

        def on_retry(self, exc, task_id, args, kwargs, einfo):
            print('Retrying...')

        def on_revoke(self, task_id, args, kwargs):
            print('Revoked :-/')
