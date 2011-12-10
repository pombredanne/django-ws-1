from __future__ import with_statement
from optparse import make_option
import socket

from django.core.management.base import BaseCommand
from django.conf import settings
from celery.events import EventReceiver
from celery.messaging import establish_connection
from celery.log import setup_logger

from ws.celery.events import CallbackState

class Command(BaseCommand):
    help = 'Listen to task events and execute tasks accordingly'
    option_list = BaseCommand.option_list + (
            make_option('-f', '--logfile', default=None,
                action='store', dest='logfile', help='Path to log file.'),
            make_option('-l', '--loglevel', default='INFO',
                action='store', dest='loglevel', 
                help='Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL'),
            )


    def handle(self, **options):
        setup_logger(name='event_receiver', 
                loglevel=options['loglevel'], logfile=options['logfile'])
        state = CallbackState()
        with establish_connection() as connection:
            while True:
                recv = EventReceiver(connection, handlers={'*': state.event})
                try:
                    recv.capture()
                except (AttributeError, socket.error):
                    connection = connection.ensure_connection()
                except KeyboardInterrupt:
                    break
                
