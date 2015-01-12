from django.test import TestCase
from django_mailbox.models import Message
from batch_apps.models import App, Day, Execution
from batch_apps.generator import get_current_date_in_gmt8
import datetime


class MessageModelTest(TestCase):

    fixtures = ['test_messages.json']

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

    def test_email_sent_time_should_be_converted_to_datetime_object_in_gmt8(self):
        email = Message.objects.get(message_id="<CAFKhJv0yhRMvdqF9JGabbHDH2Esw86Q9OZ40B52-y=MPLCyYBg@mail.gmail.com>")
        expected_object = datetime.datetime.strptime("2014-10-20 10:31:25 +0800", "%Y-%m-%d %H:%M:%S %z")
        self.assertEqual(email.sent_time, expected_object)


class DayModelTest(TestCase):

    def test_day_model_should_return_yyyy_mm_dd_as_string_representation(self):
        day = Day.objects.create(date=datetime.date(2014, 10, 20))
        self.assertEqual(day.__str__(), "2014-10-20")


class ExecutionModelTest(TestCase):

    def test_execution_model_should_return_string_for_successful_execution(self):
        app_ = App.objects.create(name="My App 001")
        day_ = Day.objects.create(date=datetime.date(2014, 10, 20))
        execution = Execution.objects.create(day=day_, app=app_, is_executed=True)
        self.assertEqual(execution.__str__(), "My App 001 executed on 2014-10-20")

    def test_execution_model_should_return_string_for_pending_execution(self):
        app_ = App.objects.create(name="My App 001")
        day_ = Day.objects.create(date=datetime.date(2014, 10, 20))
        execution = Execution.objects.create(day=day_, app=app_, is_executed=False, is_due_today=True)
        self.assertEqual(execution.__str__(), "My App 001 yet to be executed on 2014-10-20")

    def test_execution_model_should_return_string_for_inactive_execution(self):
        app_ = App.objects.create(name="My App 001")
        day_ = Day.objects.create(date=datetime.date(2014, 10, 20))
        execution = Execution.objects.create(day=day_, app=app_, is_executed=False, is_due_today=False)
        self.assertEqual(execution.__str__(), "My App 001 not to be executed on 2014-10-20")


class GenerateExecutionTest_Execution_ModelManagerTest(TestCase):

    def today(self):
        return Execution.objects.get_or_create_day_object(get_current_date_in_gmt8())

    def test_create_day_object_for_today_in_gmt8(self):
        day = self.today()
        self.assertEqual(day.date, get_current_date_in_gmt8())

    def test_create_day_object_must_return_existing_object_if_already_exists(self):
        day_existing = self.today()
        day_new = self.today()
        self.assertEqual(day_existing, day_new)

    def test_create_execution_object_for_an_app_for_today(self):
        day = self.today()
        app = App.objects.create(name='My App 001', is_active=True)
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertEqual(execution.app.name, 'My App 001')
        self.assertEqual(execution.day.date, get_current_date_in_gmt8())

    def test_create_execution_object_for_inactive_app_should_return_none(self):
        day = self.today()
        app = App.objects.create(name='My Inactive App 001', is_active=False)
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertIsNone(execution)

    def test_create_execution_objects_for_many_apps(self):
        day = self.today()
        app1 = App.objects.create(name='My App 001', is_active=True)
        app2 = App.objects.create(name='My App 002', is_active=True)
        app3 = App.objects.create(name='My App 003', is_active=True)
        apps = [app1, app2, app3]
        executions = Execution.objects.get_or_create_execution_objects(day, apps)
        self.assertEqual(executions[0].app.name, app1.name)
        self.assertEqual(executions[1].app.name, app2.name)
        self.assertEqual(executions[2].app.name, app3.name)
        self.assertEqual(executions[0].day.date, day.date)
        self.assertEqual(executions[1].day.date, day.date)
        self.assertEqual(executions[2].day.date, day.date)
        self.assertEqual(len(executions), 3)

    def test_create_execution_objects_only_for_active_apps_in_multiple_apps_list(self):
        day = self.today()
        app1 = App.objects.create(name='My App 001', is_active=True)
        app2 = App.objects.create(name='My App 002', is_active=False)
        app3 = App.objects.create(name='My App 003', is_active=True)
        apps = [app1, app2, app3]
        executions = Execution.objects.get_or_create_execution_objects(day, apps)
        self.assertEqual(executions[0].app.name, app1.name)
        self.assertEqual(executions[1].app.name, app3.name)
        self.assertEqual(executions[0].day.date, day.date)
        self.assertEqual(executions[1].day.date, day.date)
        self.assertEqual(len(executions), 2)

    def test_app_due_today_should_return_true_for_daily_frequency(self):
        app = App.objects.create(name='Daily App 001', is_active=True, frequency='daily')
        execution = Execution.objects.get_or_create_execution_object(self.today(), app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_true_for_matching_weekly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 10, 20))
        app = App.objects.create(name='Weekly Monday App 001', is_active=True, frequency='weekly - mondays')
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_false_for_non_matching_weekly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 10, 20))
        app = App.objects.create(name='Weekly Tuesday App 001', is_active=True, frequency='weekly - tuesdays')
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertFalse(execution.is_due_today)

    def test_app_due_today_should_return_true_for_matching_monthly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 11, 1))
        app = App.objects.create(name='Monthly App - Day 01', is_active=True, frequency='monthly - day 01')
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_false_for_non_matching_monthly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 11, 1))
        app = App.objects.create(name='Monthly App - Day 15', is_active=True, frequency='monthly - day 15')
        execution = Execution.objects.get_or_create_execution_object(day, app)
        self.assertFalse(execution.is_due_today)

    def test_get_day_of_week_from_string(self):
        self.assertEqual(Execution.objects.get_day_of_week_from_string('monday'), 'Monday')

    def test_get_day_of_month_from_string(self):
        self.assertEqual(Execution.objects.get_day_of_month_from_string('01'), '01')
