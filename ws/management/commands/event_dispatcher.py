from __future__ import with_statement
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from celery.log import setup_logger

from ws.celery.events import dispatch

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
        setup_logger(name='event_dispatcher', 
                loglevel=options['loglevel'], logfile=options['logfile'])
        dispatch()
