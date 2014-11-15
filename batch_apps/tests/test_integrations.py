from django.test import TestCase
from batch_apps.models import App, Day, Execution
from django_mailbox.models import Message
from batch_apps.integration import *


class AppPatternMatcherTest(TestCase):

    fixtures = ['test_apps.json']

    def test_app_matching_single_full_subject_pattern(self):
        app = App.objects.get(name="Batch App - SGEChannel doDevelopmentXML")
        pattern = app.pattern_set.filter(name_pattern="Batch App - SGEChannel doDevelopmentXML")
        self.assertTrue(app_match_full_subject(app, pattern))


class EmailExecutionAppPatternMatcherTest(TestCase):

    fixtures = ['test_apps.json', 'test_messages.json']

    def test_email_matches_single_active_daily_app_with_single_active_pattern_using_low_level_steps(self):
        app = App.objects.get(name="SGDailyAppTask SendExpiringNotice")
        self.assertTrue(app.is_active)
        self.assertEqual(app.frequency, 'daily')

        pattern_list = app.pattern_set.filter(is_active=True)
        self.assertEqual(len(pattern_list), 1)
        pattern = pattern_list[0]
        self.assertEqual(pattern.name_pattern, "SendExpiringNotice Success")
        self.assertTrue(pattern.is_active)

        day = Execution.objects.get_or_create_day_object(datetime.date(2014, 10, 20))
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertTrue(execution.is_due_today)
        self.assertFalse(execution.is_executed)

        email = Message.objects.get(message_id="<CAFKhJv21JtjnT74zzsrRuOwyEU1=1bnz2mzKV8e0_DAw0U46KA@mail.gmail.com>")
        self.assertEqual(email.subject, "Batch App - SGDailyAppTask SendExpiringNotice Success")
        self.assertEqual(str(email.sent_time), "2014-10-20 02:31:25+00:00")
        self.assertFalse(email.processed_batch_apps)
        self.assertFalse(email.matched_batch_apps)

        matched = match_subject(str(pattern), email.subject)
        self.assertTrue(matched)

        email.matched_batch_apps = True
        email.processed_batch_apps = True
        email.save()

        execution.is_executed = True
        execution.email = email
        execution.save()

        email_recheck = Message.objects.get(message_id="<CAFKhJv21JtjnT74zzsrRuOwyEU1=1bnz2mzKV8e0_DAw0U46KA@mail.gmail.com>")
        self.assertEqual(email_recheck, email)
        self.assertTrue(email_recheck.processed_batch_apps)
        self.assertTrue(email_recheck.matched_batch_apps)

        execution_recheck = Execution.objects.get_or_create_execution_object(day, app)
        self.assertTrue(execution_recheck.is_executed)
        self.assertEqual(execution_recheck.email, email)

    def test_execute_end_to_end_module_using_fixture_should_pass(self):
        app = App.objects.get(name="SGDailyAppTask SendExpiringNotice")
        self.assertTrue(app.is_active)
        self.assertEqual(app.frequency, 'daily')

        pattern_list = app.pattern_set.filter(is_active=True)
        self.assertEqual(len(pattern_list), 1)
        pattern = pattern_list[0]
        self.assertEqual(pattern.name_pattern, "SendExpiringNotice Success")
        self.assertTrue(pattern.is_active)

        email = Message.objects.get(message_id="<CAFKhJv21JtjnT74zzsrRuOwyEU1=1bnz2mzKV8e0_DAw0U46KA@mail.gmail.com>")
        self.assertEqual(email.subject, "Batch App - SGDailyAppTask SendExpiringNotice Success")
        self.assertEqual(str(email.sent_time), "2014-10-20 02:31:25+00:00")
        self.assertFalse(email.processed_batch_apps)
        self.assertFalse(email.matched_batch_apps)

        execute_end_to_end_tasks(datetime.date(2014, 10, 20))

        email_recheck = Message.objects.get(message_id="<CAFKhJv21JtjnT74zzsrRuOwyEU1=1bnz2mzKV8e0_DAw0U46KA@mail.gmail.com>")
        self.assertEqual(email_recheck, email)
        self.assertTrue(email_recheck.processed_batch_apps)
        self.assertTrue(email_recheck.matched_batch_apps)

        execution_recheck = Execution.objects.get(app=app, day__date=datetime.date(2014, 10, 20))
        self.assertTrue(execution_recheck.is_executed)
        self.assertEqual(execution_recheck.email, email)

    def test_execute_end_to_end_module_should_default_to_today_if_date_is_not_given(self):
        execute_end_to_end_tasks()
        day = Day.objects.get(pk=1)
        self.assertEqual(len(Day.objects.all()), 1)
        self.assertEqual(get_current_date_in_gmt8(), day.date)
