from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.models import App, Pattern
from batch_apps.matcher import *


class RegularExpressionTests(TestCase):

    def test_email_partial_subject_match(self):
        regex_rule = 'Batch App - Listing Refresh '
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        self.assertTrue(match_partial_prefix(regex_rule, email_subject))

    def test_email_full_subject_match(self):
        regex_rule = 'Batch App - SGEnquiryNotify sendEnquiryNotify 3 days'
        email_subject = 'Batch App - SGEnquiryNotify sendEnquiryNotify 3 days'
        self.assertTrue(match_full_subject(regex_rule, email_subject))

    def test_captured_execution_date_from_email_subject_should_return_formatted_date(self):
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        self.assertEqual(match_and_capture_date(email_subject), '2014-10-20')

    def test_captured_execution_date_should_match_any_app(self):
        email_subject = 'Batch App - Listing Archive 2010/2014'
        self.assertEqual(match_and_capture_date(email_subject), '2014-10-20')

    def test_captured_execution_date_should_match_noslash_format(self):
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        self.assertEqual(match_and_capture_date(email_subject), '2014-10-20')

    def test_captured_execution_date_should_match_slash_format(self):
        email_subject = 'Alpha and POC Listings and Co-broke Opportunities Report (20/10/2014)'
        self.assertEqual(match_and_capture_date(email_subject), '2014-10-20')


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
        self.assertTrue(app_match_full_subject(app, pattern))
