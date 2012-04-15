from __future__ import absolute_import

from celery.states import READY_STATES
from celery.registry import tasks as task_registry


STATES = dict([(s,s) for s in ('PENDING', 'RETRY', 'STARTED') + tuple(READY_STATES) ])

CONDITIONS = dict([(s,s) for s in ('XOR', 'AND')])

def get_registered_tasks():
    from celery.loaders import current_loader
    from ws.celery.tasks import BPMTask
    current_loader = current_loader()
    current_loader.import_default_modules()
    return [ key for key, value in task_registry.items()\
            if isinstance(value, BPMTask) ]
