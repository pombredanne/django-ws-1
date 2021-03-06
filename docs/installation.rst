============
Installation
============

.. todo:: pip install django-ws

WS and all needed dependencies should be installed automatically with::

    pip install hg+https://lagunak.gisa-elkartea.org/hg/django-ws


Dependencies
============

* `django_extjs4 <http://pypi.python.org/pypi/django_extjs4>`_
* `django-celery <http://pypi.python.org/pypi/django-celery>`_
* `django-guardian <http://pypi.python.org/pypi/django-celery/>`_
* `django-jsonfield <http://pypi.python.org/pypi/django-jsonfield>`_
* `pexpect <http://pypi.python.org/pypi/pexpect>`_

Also, this project uses `South <http://pypi.python.org/pypi/South>`_ to ease upgrading.

Celery needs an AMQP broker, for example `rabbitmq <http://www.rabbitmq.com/>`_


Configuration
=============

Add this to INSTALLED_APPS in project's settings.py:

* 'ws'
* 'guardian'
* 'djcelery'
* 'extjs4'


Add also the following line to your project's settings.py::

    import ws
    ws.setup_loader()


Celery configuration
--------------------

Celery has many configuration options, take a look at `celery documentation
<http://docs.celeryproject.org/en/latest/index.html>`_.

The simplest configuration requires to set the AMQP broker url. For
example::

    BROKER_URL = 'amqp://guest:guest@localhost:5672/'


Django-guardian configuration
-----------------------------

Set anonymous user's id::

    ANONYMOUS_USER_ID = -1


ExtJS administration interface
------------------------------

Include `ws.urls` somewhere in your urls::

    (r'^ws/', include('ws.urls'))


Collect the static files from `extjs4` and `ws`::

    ./manage.py collectstatic
