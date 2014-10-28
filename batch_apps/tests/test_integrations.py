from django.test import TestCase
from batch_apps.models import App
from batch_apps.matcher import *


class AppPatternMatcherTest(TestCase):

    fixtures = ['test_apps.json']

    def test_app_matching_single_full_subject_pattern(self):
        app = App.objects.get(name="Batch App - SGEChannel doDevelopmentXML")
        pattern = app.pattern_set.filter(name_pattern="Batch App - SGEChannel doDevelopmentXML")
        self.assertTrue(app_match_full_subject(app, pattern))
