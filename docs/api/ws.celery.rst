=========
ws.celery
=========

.. automodule:: ws.celery


ws.celery.bpm
=============
.. automodule:: ws.celery.bpm
.. autoclass:: ws.celery.bpm.task_started(pk, task_id)
.. autoclass:: ws.celery.bpm.task_succeeded(task_id, result)
.. autoclass:: ws.celery.bpm.task_failed(task_id)
.. autoclass:: ws.celery.bpm.task_retried(task_id)
.. autoclass:: ws.celery.bpm.task_revoked(task_id)
.. autoclass:: ws.celery.bpm.task_progress(pk, progress)


ws.celery.signals
=================
.. automodule:: ws.celery.signals


ws.celery.shortcuts
===================
.. automodule:: ws.celery.shortcuts
