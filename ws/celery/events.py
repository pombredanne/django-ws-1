from django.utils import simplejson as json

from celery.execute import send_task
from celery.events.state import State, Task


class CallbackTask(Task):
    def on_sent(self, timestamp=None, **fields):
        super(CallbackTask, self).on_sent(timestamp, **fields)
        kwargs = json.loads(self.kwargs.replace("'", '"'))
        send_task('ws.celery.bpm.task_sent', kwargs={
            'task_pk': kwargs['workflow_task'],
            'task_id': self.uuid,
            })

    def on_received(self, timestamp=None, **fields):
        super(CallbackTask, self).on_received(timestamp, **fields)
        send_task('ws.celery.bpm.task_received', kwargs={
            'task_id': self.uuid,
            })

    def on_started(self, timestamp=None, **fields):
        super(CallbackTask, self).on_started(timestamp, **fields)
        send_task('ws.celery.bpm.task_started', kwargs={
            'task_id': self.uuid,
            'timestamp': timestamp,
            })

    def on_succeeded(self, timestamp=None, **fields):
        super(CallbackTask, self).on_succeeded(timestamp, **fields)
        send_task('ws.celery.bpm.task_succeeded', kwargs={
            'task_id': self.uuid,
            'result': self.result,
            'timestamp': timestamp,
            })

    def on_failed(self, timestamp=None, **fields):
        super(CallbackTask, self).on_failed(timestamp, **fields)
        send_task('ws.celery.bpm.task_failed', kwargs={
            'task_id': self.uuid, 
            'exception': self.exception,
            'traceback': self.traceback,
            'timestamp': timestamp,
            })

    def on_revoked(self, timestamp=None, **fields):
        super(CallbackTask, self).on_revoked(timestamp, **fields)
        send_task('ws.celery.bpm.task_revoked', kwargs={
            'task_id': self.uuid,
            })

    def on_retried(self, timestamp=None, **fields):
        super(CallbackTask, self).on_retried(timestamp, **fields)
        send_task('ws.celery.bpm.task_retried', kwargs={
            'task_id': self.uuid, 
            'exception': self.exception,
            'traceback': self.traceback,
            'timestamp': timestamp,
            })


class CallbackState(State):
    def get_or_create_task(self, uuid):
        try:
            return self.tasks[uuid]
        except KeyError:
            task = self.tasks[uuid] = CallbackTask(uuid=uuid)
            return task

    def task_event(self, type, fields):
        uuid = fields.get('uuid')
        # TODO:This is a big piece of shit hack!!
        # We must be able to pickup the normal tasks by other way,
        # by routing, queue or exchange filtering.
        if self.tasks.has_key(uuid) or \
                (fields.has_key('name') and\
                fields['name'].startswith('ws.tasks')):
            super(CallbackState, self).task_event(type, fields)
        
