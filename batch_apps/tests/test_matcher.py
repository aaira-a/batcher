from django.test import TestCase
from batch_apps.matcher import *
from batch_apps.models import App, Pattern


class RegularExpressionTest(TestCase):

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

    def test_captured_execution_date_should_match_mmddyyyy_format(self):
        email_subject = 'Random App (10/20/2014)'
        self.assertEqual(capture_date(email_subject, 'mm/dd/yyyy'), '2014-10-20')

    def test_captured_execution_date_should_accommodate_single_digit_day_in_ddmmyyyy_format(self):
        email_subject = 'Random App (6/11/2014)'
        self.assertEqual(capture_date(email_subject, "dd/mm/yyyy"), '2014-11-06')

    def test_captured_execution_date_should_accommodate_single_digit_month_in_ddmmyyyy_format(self):
        email_subject = 'Random App (25/3/2014)'
        self.assertEqual(capture_date(email_subject, "dd/mm/yyyy"), '2014-03-25')

    def test_captured_execution_date_should_accommodate_single_digit_day_and_month_in_ddmmyyyy_format(self):
        email_subject = 'Random App (5/5/2014)'
        self.assertEqual(capture_date(email_subject, "dd/mm/yyyy"), '2014-05-05')

    def test_captured_execution_date_should_strip_brackets_from_supplied_pattern(self):
        email_subject = 'Random App (20/10/2014)'
        supplied_pattern = "(dd/mm/yyyy)"
        self.assertEqual(capture_date(email_subject, supplied_pattern), '2014-10-20')

    def test_captured_execution_date_should_return_none_for_unmatched_format(self):
        email_subject = 'Random App (20/10/2014)'
        supplied_pattern = "dd-mm-yyyy"
        self.assertEqual(capture_date(email_subject, supplied_pattern), None)


class EmailToAppMatcherTest(TestCase):

    def test_matcher_should_match_email_subject_to_app_with_single_active_pattern(self):
        app_ = App.objects.create(name='Simple App Identifier 001', is_active=True, frequency='daily')
        Pattern.objects.create(app=app_, name_pattern="App Identifier 001", is_active=True, is_capturing_date=False)
        email_subject = "Simple App Identifier 001 - Successfully Executed"
        self.assertTrue(match_email_subject_to_app(email_subject, app_))

    def test_matcher_should_ignore_inactive_patterns_during_matching(self):
        app_ = App.objects.create(name='Simple App Identifier 002', is_active=True, frequency='daily')
        Pattern.objects.create(app=app_, name_pattern="ActivePattern001",   is_active=True, is_capturing_date=False)
        Pattern.objects.create(app=app_, name_pattern="ActivePattern002",   is_active=True, is_capturing_date=False)
        Pattern.objects.create(app=app_, name_pattern="InactivePattern001", is_active=False, is_capturing_date=False)
        Pattern.objects.create(app=app_, name_pattern="InactivePattern002", is_active=False, is_capturing_date=False)
        email_subject = "ActivePattern001 & ActivePattern002 are matched, even if InactivePattern001 is in the subject"
        self.assertTrue(match_email_subject_to_app(email_subject, app_))

    def test_matcher_should_match_email_subject_to_all_active_patterns_for_an_app(self):
        app_ = App.objects.create(name='App Identifier 003', is_active=True, frequency='daily')
        Pattern.objects.create(app=app_, name_pattern="ABC", is_active=True, is_capturing_date=False)
        Pattern.objects.create(app=app_, name_pattern="XYZ", is_active=True, is_capturing_date=False)
        email_subject = "Email Subject - XYZ pattern and ABC pattern"
        self.assertTrue(match_email_subject_to_app(email_subject, app_))

    def test_matcher_should_return_false_if_not_all_active_patterns_are_matched(self):
        app_ = App.objects.create(name='App Identifier 004', is_active=True, frequency='daily')
        Pattern.objects.create(app=app_, name_pattern="ABC", is_active=True, is_capturing_date=False)
        Pattern.objects.create(app=app_, name_pattern="XYZ", is_active=True, is_capturing_date=False)
        email_subject = "Email Subject - XYZ pattern only, no abc.upper()"
        self.assertFalse(match_email_subject_to_app(email_subject, app_))
