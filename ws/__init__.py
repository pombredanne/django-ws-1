from celery.states import ALL_STATES

STATES = { state: state for state in ALL_STATES }
CONDITIONS = { cond: cond for cond in ('XOR', 'AND') }
