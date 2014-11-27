from django.core.management.base import BaseCommand
from django.core.management import call_command
from batch_apps.integration import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('getmail')
        execute_end_to_end_tasks()
        self.stdout.write('get_emails_and_process command executed')
