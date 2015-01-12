from django.test import TestCase
from django_mailbox.models import Message

from batch_apps.models import App, Day, Execution
from batch_apps.generator import get_current_date_in_gmt8

from batch_apps.integration import (
    execute_end_to_end_tasks,
    get_unexecuted_due_executions,
    get_unprocessed_unmatched_emails,
)

from batch_apps.matcher import match_subject

import datetime
import pytz


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


class EmailFilteringTest(TestCase):

    fixtures = ['test_messages.json']

    def setUp(self):

        self.email1 = Message.objects.get(message_id="<CAFKhJv2VAg2jx7o+Y+Kz_Ze72m7PAPq0Q8QjhC7_J+OVVnUvvg@mail.gmail.com>")
        self.email2 = Message.objects.get(message_id="<CAFKhJv1ugtTL=ji5_JxZ9KwVxfqi_haYpGb+wJrekW7RUx0pRw@mail.gmail.com>")
        self.email3 = Message.objects.get(message_id="<CAFKhJv21JtjnT74zzsrRuOwyEU1=1bnz2mzKV8e0_DAw0U46KA@mail.gmail.com>")
        self.email4 = Message.objects.get(message_id="<CAFKhJv18p+O28UB2nQT1cTKL437GFM7SJpK=30x5j7+dNRtD7A@mail.gmail.com>")
        self.email5 = Message.objects.get(message_id="<CAFKhJv0yhRMvdqF9JGabbHDH2Esw86Q9OZ40B52-y=MPLCyYBg@mail.gmail.com>")
        self.email6 = Message.objects.get(message_id="<CAG6WN+9O6P7arbVA=M1Mz=_9cSJ-nOL47eB2DaVYN_iJvc-9Lg@mail.gmail.com>")

    def test_get_unprocessed_unmatched_emails_should_return_unprocessed_emails(self):
        self.email2.processed_batch_apps = True
        self.email2.save()

        self.assertFalse(self.email1.processed_batch_apps)
        self.assertTrue(self.email2.processed_batch_apps)

        results = get_unprocessed_unmatched_emails(datetime.date(2014, 10, 20))

        self.assertIn(self.email1, results)
        self.assertNotIn(self.email2, results)

    def test_get_unprocessed_unmatched_emails_should_return_unmatched_emails(self):
        self.email4.matched_batch_apps = True
        self.email4.save()

        self.assertFalse(self.email3.matched_batch_apps)
        self.assertTrue(self.email4.matched_batch_apps)

        results = get_unprocessed_unmatched_emails(datetime.date(2014, 10, 20))

        self.assertIn(self.email3, results)
        self.assertNotIn(self.email4, results)

    def test_get_unprocessed_unmatched_emails_should_return_emails_with_correct_date(self):
        self.email6.sent_time = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
        self.email6.save()

        date_ = datetime.date(2014, 10, 20)
        results = get_unprocessed_unmatched_emails(date_)

        self.assertIn(self.email5, results)
        self.assertNotIn(self.email6, results)

    def test_get_unprocessed_unmatched_email_should_select_email_according_to_gmt8_timezone(self):
        self.email1.sent_time = datetime.datetime(2014, 11, 27, hour=15, minute=59, second=59, tzinfo=pytz.utc)
        self.email2.sent_time = datetime.datetime(2014, 11, 27, hour=16, minute=00, second=00, tzinfo=pytz.utc)
        self.email3.sent_time = datetime.datetime(2014, 11, 28, hour=15, minute=59, second=59, tzinfo=pytz.utc)
        self.email4.sent_time = datetime.datetime(2014, 11, 28, hour=16, minute=00, second=00, tzinfo=pytz.utc)

        self.email1.save()
        self.email2.save()
        self.email3.save()
        self.email4.save()

        date_ = datetime.date(2014, 11, 28)
        results = get_unprocessed_unmatched_emails(date_)

        self.assertNotIn(self.email1, results)
        self.assertIn(self.email2, results)
        self.assertIn(self.email3, results)
        self.assertNotIn(self.email4, results)


class ExecutionFilteringTest(TestCase):

    def test_get_due_executions_should_return_executions_with_correct_date(self):
        app1 = App.objects.create(name="My App 001")
        day1 = Day.objects.create(date=datetime.date(2014, 10, 20))
        day2 = Day.objects.create(date=datetime.date(2014, 10, 21))

        execution1 = Execution.objects.create(day=day1, app=app1, is_executed=False, is_due_today=True)
        execution2 = Execution.objects.create(day=day2, app=app1, is_executed=False, is_due_today=True)

        date_ = datetime.date(2014, 10, 20)
        results = get_unexecuted_due_executions(date_)
        self.assertIn(execution1, results)
        self.assertNotIn(execution2, results)

    def test_get_due_executions_should_return_executions_due_on_the_date(self):
        app1 = App.objects.create(name="My App 001")
        app2 = App.objects.create(name="My App 002")
        day = Day.objects.create(date=datetime.date(2014, 10, 20))

        execution1 = Execution.objects.create(day=day, app=app1, is_executed=False, is_due_today=True)
        execution2 = Execution.objects.create(day=day, app=app2, is_executed=False, is_due_today=False)

        date_ = datetime.date(2014, 10, 20)
        results = get_unexecuted_due_executions(date_)
        self.assertIn(execution1, results)
        self.assertNotIn(execution2, results)

    def test_get_due_executions_should_return_unexecuted_executions(self):
        app1 = App.objects.create(name="My App 001")
        app2 = App.objects.create(name="My App 002")
        day = Day.objects.create(date=datetime.date(2014, 10, 20))

        execution1 = Execution.objects.create(day=day, app=app1, is_executed=False, is_due_today=True)
        execution2 = Execution.objects.create(day=day, app=app2, is_executed=True, is_due_today=True)

        date_ = datetime.date(2014, 10, 20)
        results = get_unexecuted_due_executions(date_)
        self.assertIn(execution1, results)
        self.assertNotIn(execution2, results)
