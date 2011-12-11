from django.core.management.base import BaseCommand

from ws.celery.events import dispatch

class Command(BaseCommand):
    help = 'Listen to task events and execute tasks accordingly'

    def handle(self, **options):
        dispatch()
