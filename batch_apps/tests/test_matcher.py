from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.models import App, Pattern
import re


class RegularExpressionTests(TestCase):

    def test_simple_email_subject_match(self):
        regex_rule = 'Batch App - Listing Refresh '
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        m = re.search(regex_rule, email_subject)
        self.assertTrue(m)

    def test_capture_execution_date_from_email_subject(self):
        regex_rule = '(?:Batch App - Listing Refresh )(\d{4}/\d{4})'
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        m = re.search(regex_rule, email_subject)
        self.assertEqual(m.group(1), '2010/2014')


class EmailMatchingTests(TestCase):

    fixtures = ['test_messages.json', 'test_apps.json']

    def test_retrieve_emails_subjects_from_db(self):
        emails = Message.objects.all().order_by('id')
        expected_subjects = [
            "GPS Listings and Co-broke Opportunities Report (20/10/2014)",
            "iProperty.com Singapore Email Alert V2 - Daily Report 2010/2014",
            "Batch App - SGDailyAppTask SendExpiringNotice Success",
            "Batch App - Listing Archive 2010/2014",
            "Batch App - SGEChannel doDevelopmentXML"
        ]
        for email in emails:
            self.assertIn(email.subject, expected_subjects)

    def test_app_matching_single_full_subject_pattern(self):
        app = App.objects.get(name="Batch App - SGEChannel doDevelopmentXML")
        pattern = app.pattern_set.filter(pattern_string="Batch App - SGEChannel doDevelopmentXML")
        m = re.search(str(pattern), str(app))
        self.assertTrue(m)
