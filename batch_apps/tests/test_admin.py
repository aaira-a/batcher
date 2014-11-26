from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from batch_apps.models import App
from batch_apps.admin import AppAdmin


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
