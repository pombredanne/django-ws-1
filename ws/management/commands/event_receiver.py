from __future__ import with_statement

import socket

from django.core.management.base import NoArgsCommand

from celery.events import EventReceiver
from celery.messaging import establish_connection

from ws.celery.events import CallbackState

class Command(NoArgsCommand):
    help = 'Listen to task events and execute tasks accordingly'

    def handle_noargs(self, **options):
        state = CallbackState()
        with establish_connection() as connection:
            while True:
                recv = EventReceiver(connection, handlers={'*': state.event})
                try:
                    recv.capture(limit=None, timeout=None)
                except (AttributeError, socket.error):
                    connection = connection.ensure_connection()
                
