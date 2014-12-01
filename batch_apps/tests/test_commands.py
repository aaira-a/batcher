from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO


class GetEmailsAndProcessCommandTest(TestCase):

    def test_process_emails_command_should_be_launchable_using_call_command(self):
        output = StringIO()
        call_command('get_emails_and_process', stdout=output)
        self.assertIn('get_emails_and_process command executed', output.getvalue())


class ProcessPreviousDayEmailTest(TestCase):

    def test_process_previous_day_email_command_should_be_launchable_using_call_command(self):
        output = StringIO()
        call_command('process_previous_day', stdout=output)
        self.assertIn('process_previous_day command executed', output.getvalue())
