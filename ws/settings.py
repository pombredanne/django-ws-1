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
