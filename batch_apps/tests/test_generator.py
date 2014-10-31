from django.test import TestCase
from batch_apps.generator import *
from pytz import timezone


class GenerateDayTest(TestCase):

    def test_get_current_date_in_gmt8(self):
        datetime_utc = datetime.datetime.now(pytz.utc)
        converted_datetime = datetime_utc.astimezone((timezone('Asia/Kuala_Lumpur')))
        self.assertEqual(get_current_date_in_gmt8(), converted_datetime.date())

    def test_create_day_object_for_today_in_gmt8(self):
        day = create_day_object(get_current_date_in_gmt8())
        self.assertEqual(day.date, get_current_date_in_gmt8())

    def test_create_day_object_must_return_existing_object_if_already_exists(self):
        day_existing = create_day_object(get_current_date_in_gmt8())
        day_new = create_day_object(get_current_date_in_gmt8())
        self.assertEqual(day_existing, day_new)
