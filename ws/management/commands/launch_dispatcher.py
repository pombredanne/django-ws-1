from django.core.management.base import BaseCommand

from ws.celery.bpm import dispatcher

class Command(BaseCommand):
    help = 'Launch a task that will listen to task events and execute tasks accordingly'

    def handle(self, **options):
        dispatcher.apply_async()
