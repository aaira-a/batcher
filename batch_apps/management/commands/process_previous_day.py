from django.core.management.base import BaseCommand
from batch_apps.integration import execute_end_to_end_tasks
from batch_apps.generator import get_current_date_in_gmt8
import datetime


today = get_current_date_in_gmt8()
yesterday = today + datetime.timedelta(days=-1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute_end_to_end_tasks(yesterday)
        self.stdout.write('process_previous_day command executed')
