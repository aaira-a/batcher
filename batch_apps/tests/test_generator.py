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
