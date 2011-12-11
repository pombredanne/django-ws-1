import socket
from django.utils import simplejson as json

from celery.execute import send_task
from celery.events import EventReceiver, Queue, event_exchange
from celery.events.state import State, Task
from celery.utils.term import colored
from celery.log import get_default_logger
from celery.messaging import establish_connection

logger = get_default_logger(name='event_dispatcher')
c = colored()

class CallbackTask(Task):
    def on_sent(self, timestamp=None, **fields):
        super(CallbackTask, self).on_sent(timestamp, **fields)
        kwargs = json.loads(self.kwargs.replace("'", '"'))
        send_task('ws.celery.bpm.task_sent', kwargs={
            'task_pk': kwargs['workflow_task'],
            'task_id': self.uuid,
            })
        logger.info('{state}: {task}'.format(
            state=c.bold('SENT'),
            task=self.name,
            ))

    def on_received(self, timestamp=None, **fields):
        super(CallbackTask, self).on_received(timestamp, **fields)
        send_task('ws.celery.bpm.task_received', kwargs={
            'task_id': self.uuid,
            })
        logger.info('{state}: {task} at {hostname}'.format(
            state=c.bold('RECEIVED'),
            task=self.name, 
            hostname=fields.get('hostname', 'localhost')
            ))

    def on_started(self, timestamp=None, **fields):
        super(CallbackTask, self).on_started(timestamp, **fields)
        send_task('ws.celery.bpm.task_started', kwargs={
            'task_id': self.uuid,
            'timestamp': timestamp,
            })
        logger.info('{state}: {task} at {hostname} with PID {pid}'.format(
            state=c.bold('STARTED'),
            task=self.name, 
            hostname=fields.get('hostname', 'localhost'),
            pid=fields.get('pid', 'UNKNOWN'),
            ))

    def on_succeeded(self, timestamp=None, **fields):
        super(CallbackTask, self).on_succeeded(timestamp, **fields)
        send_task('ws.celery.bpm.task_succeeded', kwargs={
            'task_id': self.uuid,
            'result': self.result,
            'timestamp': timestamp,
            })
        logger.info(('{state}: {task} at {hostname} with result {result}'
            ' after {runtime} seconds').format(
            state=c.bold('SUCCEEDED'),
            task=self.name, 
            hostname=fields.get('hostname', 'localhost'),
            result=fields.get('result', 'None'),
            runtime=fields.get('runtime', 0),
            ))

    def on_failed(self, timestamp=None, **fields):
        super(CallbackTask, self).on_failed(timestamp, **fields)
        send_task('ws.celery.bpm.task_failed', kwargs={
            'task_id': self.uuid, 
            'exception': self.exception,
            'traceback': self.traceback,
            'timestamp': timestamp,
            })
        logger.warn(('{state}: {task} at {hostname} with exception'
            ' {exception}').format(
            state=c.bold('FAILED'),
            task=self.name, 
            hostname=fields.get('hostname', 'localhost'),
            exception=fields.get('exception'),
            ))

    def on_revoked(self, timestamp=None, **fields):
        super(CallbackTask, self).on_revoked(timestamp, **fields)
        send_task('ws.celery.bpm.task_revoked', kwargs={
            'task_id': self.uuid,
            })
        logger.warn(('{state}: {task}').format(
            state=c.bold('REVOKED'),
            task=self.name, 
            ))

    def on_retried(self, timestamp=None, **fields):
        super(CallbackTask, self).on_retried(timestamp, **fields)
        send_task('ws.celery.bpm.task_retried', kwargs={
            'task_id': self.uuid, 
            'exception': self.exception,
            'traceback': self.traceback,
            'timestamp': timestamp,
            })
        logger.warn(('{state}: {task} at {hostname} with exception'
            ' {exception}').format(
            state=c.bold('RETRIED'),
            task=self.name, 
            hostname=fields.get('hostname', 'localhost'),
            exception=fields.get('exception'),
            ))


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


class DurableEventReceiver(EventReceiver):
    def __init__(self, *args, **kwargs):
        super(DurableEventReceiver, self).__init__(*args, **kwargs)
        self.queue = Queue('celeryev.dispatcher', durable=True,
                exchange=event_exchange, routing_key=self.routing_key)

def dispatch():
    state = CallbackState()
    with establish_connection() as connection:
        while True:
            recv = DurableEventReceiver(connection, handlers={'*': state.event})
            try:
                recv.capture()
            except (AttributeError, socket.error):
                connection = connection.ensure_connection()
