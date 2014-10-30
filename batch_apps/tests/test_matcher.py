from django.test import TestCase
from batch_apps.matcher import *


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

    def test_captured_execution_date_should_strip_brackets_from_supplied_pattern(self):
        email_subject = 'Random App (20/10/2014)'
        supplied_pattern = "(dd/mm/yyyy)"
        self.assertEqual(capture_date(email_subject, supplied_pattern), '2014-10-20')

    def test_captured_execution_date_should_return_none_for_unmatched_format(self):
        email_subject = 'Random App (20/10/2014)'
        supplied_pattern = "dd-mm-yyyy"
        self.assertEqual(capture_date(email_subject, supplied_pattern), None)
