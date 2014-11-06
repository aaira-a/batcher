from django.test import TestCase


class ExecutionsViewTest(TestCase):

    def test_executions_view_renders_executions_template(self):
        response = self.client.get('/executions/')
        self.assertTemplateUsed(response, 'executions.html')

    def test_url_specific_execution_date_renders_execution_template(self):
        response = self.client.get('/executions/2014-11-03/')
        self.assertTemplateUsed(response, 'executions.html')
