from __future__ import absolute_import
from celery.states import ALL_STATES

STATES = dict([(s,s) for s in ALL_STATES])
CONDITIONS = dict([(s,s) for s in ('XOR', 'AND')])
