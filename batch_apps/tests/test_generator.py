from django.test import TestCase
from batch_apps.generator import *
from batch_apps.models import App
from pytz import timezone
import datetime


def today():
    return get_or_create_day_object(get_current_date_in_gmt8())


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

    def test_date_from_str_should_return_date_object_from_iso_format_string(self):
        expected_date_object = datetime.datetime.strptime('2014-11-25', "%Y-%m-%d").date()
        self.assertEqual(date_from_str('2014-11-25'), expected_date_object)

    def test_date_to_str_should_return_iso_format_string_from_date_object(self):
        date_object = datetime.datetime.strptime('2014-11-27', "%Y-%m-%d").date()
        self.assertEqual(date_to_str(date_object), '2014-11-27')


class GenerateWeekTest(TestCase):

    def test_generate_week_with_date_ending_should_return_ascending_dates_list(self):
        dates = generate_one_week_date('2014-11-11')
        self.assertEqual(dates[0].strftime("%Y-%m-%d"), '2014-11-05')
        self.assertEqual(dates[1].strftime("%Y-%m-%d"), '2014-11-06')
        self.assertEqual(dates[2].strftime("%Y-%m-%d"), '2014-11-07')
        self.assertEqual(dates[3].strftime("%Y-%m-%d"), '2014-11-08')
        self.assertEqual(dates[4].strftime("%Y-%m-%d"), '2014-11-09')
        self.assertEqual(dates[5].strftime("%Y-%m-%d"), '2014-11-10')
        self.assertEqual(dates[6].strftime("%Y-%m-%d"), '2014-11-11')

    def test_generate_week_with_date_ending_should_work_across_months(self):
        dates = generate_one_week_date('2014-11-03')
        self.assertEqual(dates[0].strftime("%Y-%m-%d"), '2014-10-28')
        self.assertEqual(dates[1].strftime("%Y-%m-%d"), '2014-10-29')
        self.assertEqual(dates[2].strftime("%Y-%m-%d"), '2014-10-30')
        self.assertEqual(dates[3].strftime("%Y-%m-%d"), '2014-10-31')
        self.assertEqual(dates[4].strftime("%Y-%m-%d"), '2014-11-01')
        self.assertEqual(dates[5].strftime("%Y-%m-%d"), '2014-11-02')
        self.assertEqual(dates[6].strftime("%Y-%m-%d"), '2014-11-03')


class GenerateExecutionTest(TestCase):

    def test_create_execution_object_for_an_app_for_today(self):
        day = today()
        app = App.objects.create(name='My App 001', is_active=True)
        execution = get_or_create_execution_object(day, app)
        self.assertEqual(execution.app.name, 'My App 001')
        self.assertEqual(execution.day.date, get_current_date_in_gmt8())

    def test_create_execution_object_for_inactive_app_should_return_none(self):
        day = today()
        app = App.objects.create(name='My Inactive App 001', is_active=False)
        execution = get_or_create_execution_object(day, app)
        self.assertIsNone(execution)

    def test_create_execution_objects_for_many_apps(self):
        day = today()
        app1 = App.objects.create(name='My App 001', is_active=True)
        app2 = App.objects.create(name='My App 002', is_active=True)
        app3 = App.objects.create(name='My App 003', is_active=True)
        apps = [app1, app2, app3]
        executions = get_or_create_execution_objects(day, apps)
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
        executions = get_or_create_execution_objects(day, apps)
        self.assertEqual(executions[0].app.name, app1.name)
        self.assertEqual(executions[1].app.name, app3.name)
        self.assertEqual(executions[0].day.date, day.date)
        self.assertEqual(executions[1].day.date, day.date)
        self.assertEqual(len(executions), 2)

    def test_app_due_today_should_return_true_for_daily_frequency(self):
        app = App.objects.create(name='Daily App 001', is_active=True, frequency='daily')
        execution = get_or_create_execution_object(today(), app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_true_for_matching_weekly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 10, 20))
        app = App.objects.create(name='Weekly Monday App 001', is_active=True, frequency='weekly - mondays')
        execution = get_or_create_execution_object(day, app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_false_for_non_matching_weekly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 10, 20))
        app = App.objects.create(name='Weekly Tuesday App 001', is_active=True, frequency='weekly - tuesdays')
        execution = get_or_create_execution_object(day, app)
        self.assertFalse(execution.is_due_today)

    def test_app_due_today_should_return_true_for_matching_monthly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 11, 1))
        app = App.objects.create(name='Monthly App - Day 01', is_active=True, frequency='monthly - day 01')
        execution = get_or_create_execution_object(day, app)
        self.assertTrue(execution.is_due_today)

    def test_app_due_today_should_return_false_for_non_matching_monthly_day(self):
        day = Day.objects.create(date=datetime.date(2014, 11, 1))
        app = App.objects.create(name='Monthly App - Day 15', is_active=True, frequency='monthly - day 15')
        execution = get_or_create_execution_object(day, app)
        self.assertFalse(execution.is_due_today)

    def test_get_day_of_week_from_string(self):
        self.assertEqual(get_day_of_week_from_string('monday'), 'Monday')

    def test_get_day_of_month_from_string(self):
        self.assertEqual(get_day_of_month_from_string('01'), '01')
