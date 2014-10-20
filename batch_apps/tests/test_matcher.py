from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.models import App, Pattern
import re


class RegularExpressionTests(TestCase):
    def test_simple_email_subject_match(self):
        regex_string = 'Batch App - Listing Refresh '
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        m = re.search(regex_string, email_subject)
        self.assertTrue(m)

    def test_capture_execution_date_from_email_subject(self):
        regex_string = 'Batch App - Listing Refresh '
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        m = re.search('(?:Batch App - Listing Refresh )(\d{4}/\d{4})', email_subject)
        self.assertEqual(m.group(1), '2010/2014')
