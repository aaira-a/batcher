from django.test import TestCase
from batch_apps.generator import *
from batch_apps.models import App
from pytz import timezone


def today():
    return create_day_object(get_current_date_in_gmt8())


class GenerateDayTest(TestCase):

    def test_get_current_date_in_gmt8(self):
        datetime_utc = datetime.datetime.now(pytz.utc)
        converted_datetime = datetime_utc.astimezone((timezone('Asia/Kuala_Lumpur')))
        self.assertEqual(get_current_date_in_gmt8(), converted_datetime.date())

    def test_create_day_object_for_today_in_gmt8(self):
        day = today()
        self.assertEqual(day.date, get_current_date_in_gmt8())

    def test_create_day_object_must_return_existing_object_if_already_exists(self):
        day_existing = today()
        day_new = today()
        self.assertEqual(day_existing, day_new)


class GenerateExecutionTest(TestCase):

    def test_create_execution_object_for_an_app_for_today(self):
        day = today()
        app = App.objects.create(name='My App 001', is_active=True)
        execution = create_execution_object(day, app)
        self.assertEqual(execution.app.name, 'My App 001')
        self.assertEqual(execution.day.date, get_current_date_in_gmt8())

    def test_create_execution_object_for_inactive_app_should_return_none(self):
        day = today()
        app = App.objects.create(name='My Inactive App 001', is_active=False)
        execution = create_execution_object(day, app)
        self.assertIsNone(execution)

    def test_create_execution_objects_for_many_apps(self):
        day = today()
        app1 = App.objects.create(name='My App 001', is_active=True)
        app2 = App.objects.create(name='My App 002', is_active=True)
        app3 = App.objects.create(name='My App 003', is_active=True)
        apps = [app1, app2, app3]
        executions = create_execution_objects(day, apps)
        self.assertEqual(executions[0].app.name, app1.name)
        self.assertEqual(executions[1].app.name, app2.name)
        self.assertEqual(executions[2].app.name, app3.name)
        self.assertEqual(executions[0].day.date, day.date)
        self.assertEqual(executions[1].day.date, day.date)
        self.assertEqual(executions[2].day.date, day.date)
        self.assertEqual(len(executions), 3)

    def test_create_execution_objects_only_for_active_apps_in_multiple_apps_list(self):
        day = today()
        app1 = App.objects.create(name='My App 001', is_active=True)
        app2 = App.objects.create(name='My App 002', is_active=False)
        app3 = App.objects.create(name='My App 003', is_active=True)
        apps = [app1, app2, app3]
        executions = create_execution_objects(day, apps)
        self.assertEqual(executions[0].app.name, app1.name)
        self.assertEqual(executions[1].app.name, app3.name)
        self.assertEqual(executions[0].day.date, day.date)
        self.assertEqual(executions[1].day.date, day.date)
        self.assertEqual(len(executions), 2)

    def test_app_due_today_should_return_true_for_daily_frequency(self):
        app = App.objects.create(name='Daily App 001', is_active=True, frequency='daily')
        execution = create_execution_object(today(), app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_true_for_matching_weekly_day(self):
        fail

    def test_app_due_today_should_return_false_for_non_matching_weekly_day(self):
        fail

    def test_app_due_today_should_return_true_for_matching_monthly_day(self):
        fail

    def test_app_due_today_should_return_false_for_non_matching_monthly_day(self):
        fail
