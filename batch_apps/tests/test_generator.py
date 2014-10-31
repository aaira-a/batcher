from django.test import TestCase
from batch_apps.generator import *
from pytz import timezone


class GenerateDayTest(TestCase):

    def test_get_current_date_in_gmt8(self):
        datetime_utc = datetime.datetime.now(pytz.utc)
        converted_datetime = datetime_utc.astimezone((timezone('Asia/Kuala_Lumpur')))
        self.assertEqual(get_current_date_in_gmt8(self), converted_datetime.date())
