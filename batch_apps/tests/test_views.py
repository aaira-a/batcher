from django.test import TestCase


class ExecutionsViewTest(TestCase):

    def test_executions_view_renders_executions_template(self):
        response = self.client.get('/executions/')
        self.assertTemplateUsed(response, 'executions.html')
