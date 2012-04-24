##################################################################################
#  Copyright 2011,2012 GISA Elkartea.                                            #
#                                                                                #
#  This file is part of django-ws.                                               #
#                                                                                #
#  django-ws is free software: you can redistribute it and/or modify it under    #
#  the terms of the GNU Affero General Public License as published by the Free   #
#  Software Foundation, either version 3 of the License, or (at your option)     #
#  any later version.                                                            #
#                                                                                #
#  django-ws is distributed in the hope that it will be useful, but WITHOUT ANY  #
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS     #
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for      #
#  more details.                                                                 #
#                                                                                #
#  You should have received a copy of the GNU Affero General Public License      #
#  along with django-ws. If not, see <http://www.gnu.org/licenses/>.             #
##################################################################################

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'guardian.backends.ObjectPermissionBackend',
        )

LOGIN_URL = '/ws/login'
ANONYMOUS_USER_ID = 1

import djcelery
djcelery.setup_loader()
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
CELERY_IMPORTS = 'ws.tasks', 'ws.celery.bpm'
CELERY_RESULT_BACKEND = 'amqp'
#CELERYD_HIJACK_ROOT_LOGGER = False
