============
Installation
============

.. note:: *(future)* pip install django-ws

django-ws and all needed dependencies should be installed automatically with::

    pip install hg+https://lagunak.gisa-elkartea.org/hg/django-ws


Dependencies
============

* `django_extjs4 <http://pypi.python.org/pypi/django_extjs4>`_
* `django-celery <http://pypi.python.org/pypi/django-celery>`_
* `django-guardian <http://pypi.python.org/pypi/django-celery/>`_
* `django-jsonfield <http://pypi.python.org/pypi/django-jsonfield>`_
* `pexpect <http://pypi.python.org/pypi/pexpect>`_

Also, this project uses `South <http://pypi.python.org/pypi/South>`_ to ease upgrading.


Configuration
=============

Add this to INSTALLED_APPS in project's settings.py:

* 'ws'
* 'django-guardian'
* 'djcelery'
* 'extjs4'

Configure Celery and add 'ws.tasks' and 'ws.celery.bpm' to CELERY_IMPORTS

For inpatients, ws.settings module has default values. You could add this
to your project's settings.py::

    from ws.settings import *
