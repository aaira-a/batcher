from django.test import TestCase
from batch_apps.generator import *
from batch_apps.models import App
from pytz import timezone


class GenerateDayTest(TestCase):

    def test_get_current_date_in_gmt8(self):
        datetime_utc = datetime.datetime.now(pytz.utc)
        converted_datetime = datetime_utc.astimezone((timezone('Asia/Kuala_Lumpur')))
        self.assertEqual(get_current_date_in_gmt8(), converted_datetime.date())

    def test_create_day_object_for_today_in_gmt8(self):
        day = create_day_object(get_current_date_in_gmt8())
        self.assertEqual(day.date, get_current_date_in_gmt8())

    def test_create_day_object_must_return_existing_object_if_already_exists(self):
        day_existing = create_day_object(get_current_date_in_gmt8())
        day_new = create_day_object(get_current_date_in_gmt8())
        self.assertEqual(day_existing, day_new)


class GenerateExecutionTest(TestCase):

    def test_create_execution_object_for_an_app_for_today(self):
        day = create_day_object(get_current_date_in_gmt8())
        app = App.objects.create(name='My App 001', is_active=True)
        execution = create_execution_object(day, app)
        self.assertEqual(execution.app.name, 'My App 001')
        self.assertEqual(execution.day.date, get_current_date_in_gmt8())

    def test_create_execution_object_for_inactive_app_should_return_none(self):
        day = create_day_object(get_current_date_in_gmt8())
        app = App.objects.create(name='My Inactive App 001', is_active=False)
        execution = create_execution_object(day, app)
        self.assertIsNone(execution)

    def test_create_execution_objects_for_many_apps(self):
        day = create_day_object(get_current_date_in_gmt8())
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
        day = create_day_object(get_current_date_in_gmt8())
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
