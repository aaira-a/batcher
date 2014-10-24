from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.models import App, Pattern
from batch_apps.matcher import *


class RegularExpressionTests(TestCase):

    def test_email_partial_subject_match(self):
        regex_rule = 'Batch App - Listing Refresh '
        email_subject = 'Batch App - Listing Refresh 2010/2014'
        self.assertTrue(match_subject(regex_rule, email_subject))

    def test_email_full_subject_match(self):
        regex_rule = 'Batch App - SGEnquiryNotify sendEnquiryNotify 3 days'
        email_subject = 'Batch App - SGEnquiryNotify sendEnquiryNotify 3 days'
        self.assertTrue(match_subject(regex_rule, email_subject))

    def test_captured_execution_date_from_email_subject_should_return_formatted_date(self):
        email_subject = 'Random App (20/10/2014)'
        self.assertEqual(capture_date(email_subject), '2014-10-20')

    def test_captured_execution_date_should_allow_user_supplied_pattern(self):
        email_subject = 'Random App (1020/2014)'
        supplied_pattern = "mmdd/yyyy"
        self.assertEqual(capture_date(email_subject, supplied_pattern), '2014-10-20')

    def test_captured_execution_date_should_match_any_app(self):
        email_subject = 'Different Named App 20/10/2014'
        self.assertEqual(capture_date(email_subject, 'dd/mm/yyyy'), '2014-10-20')

    def test_captured_execution_date_should_match_noslash_format(self):
        email_subject = 'Random App 2010/2014'
        self.assertEqual(capture_date(email_subject, 'ddmm/yyyy'), '2014-10-20')

    def test_captured_execution_date_should_match_slash_format(self):
        email_subject = 'Random App (20/10/2014)'
        self.assertEqual(capture_date(email_subject), '2014-10-20')

    def test_captured_execution_date_should_strip_brackets_from_supplied_pattern(self):
        email_subject = 'Random App (20/10/2014)'
        supplied_pattern = "(dd/mm/yyyy)"
        self.assertEqual(capture_date(email_subject, supplied_pattern), '2014-10-20')


class EmailMatchingTests(TestCase):

    fixtures = ['test_messages.json', 'test_apps.json']

    def test_retrieve_emails_subjects_from_db(self):
        emails = Message.objects.all().order_by('id')
        expected_subjects = [
            "GPS Listings and Co-broke Opportunities Report (20/10/2014)",
            "iProperty.com Singapore Email Alert V2 - Daily Report 2010/2014",
            "Batch App - SGDailyAppTask SendExpiringNotice Success",
            "Batch App - Listing Archive 2010/2014",
            "Batch App - SGEChannel doDevelopmentXML",
            "test email sent at 2014-10-23 1739 gmt +8 and 0939 at utc",
        ]
        for email in emails:
            self.assertIn(email.subject, expected_subjects)

    def test_app_matching_single_full_subject_pattern(self):
        app = App.objects.get(name="Batch App - SGEChannel doDevelopmentXML")
        pattern = app.pattern_set.filter(name_pattern="Batch App - SGEChannel doDevelopmentXML")
        self.assertTrue(app_match_full_subject(app, pattern))

    def test_email_sent_time_should_be_converted_to_datetime_object_in_gmt8(self):
        email = Message.objects.get(sent_time="Thu, 23 Oct 2014 17:37:52 +0800")
        expected_object = datetime.datetime.strptime("2014-10-23 17:37:52 +0800", "%Y-%m-%d %H:%M:%S %z")
        self.assertEqual(convert_sent_time_string_to_datetime_object(email.sent_time), expected_object)
