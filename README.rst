====================
Django WorkSheet BPM
====================

A Business Process Manager for Django. Uses Celery for task automation and
ExtJS for web interface.


Instalation
===========

The code is developed and tested in Django 1.4 and RabbitMQ 2.8.

All the dependencies should be installed automatically:

* django_extjs4
* django-celery
* django-guardian
* django-jsonfield

Also, this project uses South to ease upgrading.


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


License
=======

django-ws is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

See LICENSE file for full license details.
