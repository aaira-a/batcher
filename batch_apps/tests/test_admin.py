from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from batch_apps.models import App, Day, Execution
from batch_apps.admin import AppAdmin, DayAdmin
import datetime


class MockRequest(object):
    pass

request = MockRequest()


class AppAdminTest(TestCase):

    def setUp(self):
        self.app_admin = AppAdmin(App, AdminSite())

    def test_activate_apps_should_activate_inactive_app(self):
        app1 = App.objects.create(name='Inactive App 001', is_active=False)
        queryset = App.objects.filter(pk=1)
        self.app_admin.activate_apps(request, queryset)
        self.assertTrue(App.objects.get(pk=1).is_active)

    def test_deactivate_apps_should_deactivate_active_app(self):
        app1 = App.objects.create(name='Active App 001', is_active=True)
        queryset = App.objects.filter(pk=1)
        self.app_admin.deactivate_apps(request, queryset)
        self.assertFalse(App.objects.get(pk=1).is_active)


class DayAdminTest(TestCase):

    def setUp(self):
        self.day_admin = DayAdmin(Day, AdminSite())

    def test_execute_end_to_end_tasks_on_day_should_generate_execution_objects(self):
        date_ = datetime.date(2014, 10, 20)
        day = Day.objects.create(date=date_)

        app1 = App.objects.create(name='Daily App 001', is_active=True)
        queryset = Day.objects.filter(pk=1)

        self.day_admin.execute_end_to_end_tasks_on_day(request, queryset)
        execution = Execution.objects.get(pk=1)
        self.assertEqual(execution.app, app1)
        self.assertEqual(execution.day.date, date_)
