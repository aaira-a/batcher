from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from batch_apps.models import App
from batch_apps.admin import AppAdmin


class MockRequest(object):
    pass

request = MockRequest()


class AppAdminTest(TestCase):

    def test_activate_apps_admin_action_should_return_activated(self):
        app_admin = AppAdmin(App, AdminSite())
        queryset = app_admin.get_queryset(request)
        self.assertEqual(app_admin.activate_apps(request, queryset), 'activated')

    def test_deactivate_apps_admin_action_should_return_deactivated(self):
        app_admin = AppAdmin(App, AdminSite())
        queryset = app_admin.get_queryset(request)
        self.assertTrue(app_admin.deactivate_apps(request, queryset), 'deactivated')
