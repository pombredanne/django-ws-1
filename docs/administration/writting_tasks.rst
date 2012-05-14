===================
Custom celery tasks
===================

WS task's are celery tasks inheriting :class:`BPMTask`. They must be in a
module loaded by celery, the typical place it's a tasks.py file in
the django application's root. It's strongly recommended to define also a
form describing the task's parameters, but not strictly necessary::

    from ws.tasks import BPMTask
    from ws import forms

    class MultiplyTaskForm(forms.BPMTaskForm):
        a = forms.IntegerField(label='first number')
        b = forms.IntegerField(label='second number')


    class MultiplyTask(BPMTask):
        form = MultiplyTaskForm
        
        def call(self, a, b):
            return a * b

Note that :mod:`ws.forms` module is used instead :mod:`django.forms`. :mod:`ws.forms` are
basically ExtJS enabled :mod:`django.forms`.

It's also possible to define certain actions that will take place when certain events happen::

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
