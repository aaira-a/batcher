from django.test import TestCase
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
        self.assertContains(response, "Oct. 24, 2014")
        self.assertContains(response, "Oct. 25, 2014")
        self.assertContains(response, "Oct. 26, 2014")
        self.assertContains(response, "Oct. 27, 2014")
        self.assertContains(response, "Oct. 28, 2014")
        self.assertContains(response, "Oct. 29, 2014")
        self.assertContains(response, "Oct. 30, 2014")

    def test_weekly_execution_view_should_return_404_for_date_more_than_today(self):
        today = get_current_date_in_gmt8()
        tomorrow = today + datetime.timedelta(days=1)
        response = self.client.get('/executions/week/' + tomorrow.strftime("%Y-%m-%d") + '/')
        self.assertEqual(response.status_code, 404)
