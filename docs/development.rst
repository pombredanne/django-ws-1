===============================
Development, Help & Suggestions
===============================

WS is hosted in a `redmine <http://www.redmine.org>`_ project on
http://lagunak.gisa-elkartea.org/projects/django-ws

Reporting bugs and suggestions
==============================

Use the `issue tracker <http://lagunak.gisa-elkartea.org/projects/django-ws/issues>`_.

Asking for help 
===============

There is a `forum <http://lagunak.gisa-elkartea.org/projects/django-ws/boards>`_
ready for questions. Preferred language is english, but basque or spanish
questions are also welcomed.


Getting source code
===================

The code is in a `mercurial <http://mercurial.selenic.com/>`_ repository::

    hg clone https://lagunak.gisa-elkartea.org/hg/django-ws


Testing
=======

The code is developed and tested in Django 1.4 and RabbitMQ 2.8.

Many tests require a working celery environment. You could run celeryd and
the AMQP broker or set the celery's test runner::

    TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
