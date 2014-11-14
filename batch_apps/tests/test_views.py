from django.test import TestCase
from batch_apps.models import App
from batch_apps.generator import *
import datetime


class ExecutionsViewTest(TestCase):

    def test_executions_view_renders_executions_template(self):
        response = self.client.get('/executions/')
        self.assertTemplateUsed(response, 'executions.html')

    def test_view_should_return_404_if_there_is_unspecified_trailing_characters(self):
        response = self.client.get('/executions/1wh4t3v3r')
        self.assertEqual(response.status_code, 404)

    def test_url_specific_execution_date_renders_execution_template(self):
        response = self.client.get('/executions/2014-11-03/')
        self.assertTemplateUsed(response, 'executions.html')

    def test_specific_date_execution_view_should_render_for_correct_date_context(self):
        response = self.client.get('/executions/2014-10-25/')
        self.assertContains(response, "Oct. 25, 2014")

    def test_execution_view_should_return_404_for_date_more_than_today(self):
        today = get_current_date_in_gmt8()
        tomorrow = today + datetime.timedelta(days=1)
        response = self.client.get('/executions/' + tomorrow.strftime("%Y-%m-%d") + '/')
        self.assertEqual(response.status_code, 404)


class WeeklyExecutionsViewTest(TestCase):

    def test_weekly_executions_view_renders_executions_template(self):
        response = self.client.get('/executions/week/2014-10-30/')
        self.assertTemplateUsed(response, 'executions_week.html')

    def test_weekly_view_should_return_404_if_there_is_unspecified_trailing_characters(self):
        response = self.client.get('/executions/week/2014-10-30/extra')
        self.assertEqual(response.status_code, 404)

    def test_weekly_execution_view_should_render_for_correct_date_context(self):
        response = self.client.get('/executions/week/2014-10-30/')
        self.assertContains(response, "2014-10-24")
        self.assertContains(response, "2014-10-25")
        self.assertContains(response, "2014-10-26")
        self.assertContains(response, "2014-10-27")
        self.assertContains(response, "2014-10-28")
        self.assertContains(response, "2014-10-29")
        self.assertContains(response, "2014-10-30")

    def test_weekly_execution_view_should_return_404_for_date_more_than_today(self):
        today = get_current_date_in_gmt8()
        tomorrow = today + datetime.timedelta(days=1)
        response = self.client.get('/executions/week/' + tomorrow.strftime("%Y-%m-%d") + '/')
        self.assertEqual(response.status_code, 404)

    def test_weekly_executions_view_should_render_daily_app_execution_status_for_whole_week(self):
        app1 = App.objects.create(name='Daily App 001', is_active=True, frequency='daily')
        response = self.client.get('/executions/week/2014-10-25/')
        self.assertContains(response, 'Daily App 001')
        self.assertContains(response, 'is_due_True is_executed_False', count=7)

    def test_weekly_executions_view_should_render_weekly_app_execution_status_for_whole_week(self):
        app1 = App.objects.create(name='Weekly App 001', is_active=True, frequency='weekly - wednesdays')
        response = self.client.get('/executions/week/2014-10-25/')
        self.assertContains(response, 'Weekly App 001')
        self.assertContains(response, 'is_due_False is_executed_False', count=6)
