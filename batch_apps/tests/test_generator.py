from django.test import TestCase
from batch_apps.generator import *
from pytz import timezone
import datetime


class GenerateDateTest(TestCase):

    def test_get_current_date_in_gmt8(self):
        datetime_utc = datetime.datetime.now(pytz.utc)
        converted_datetime = datetime_utc.astimezone((timezone('Asia/Kuala_Lumpur')))
        self.assertEqual(get_current_date_in_gmt8(), converted_datetime.date())

    def test_date_from_str_should_return_date_object_from_iso_format_string(self):
        expected_date_object = datetime.datetime.strptime('2014-11-25', "%Y-%m-%d").date()
        self.assertEqual(date_from_str('2014-11-25'), expected_date_object)

    def test_date_to_str_should_return_iso_format_string_from_date_object(self):
        date_object = datetime.datetime.strptime('2014-11-27', "%Y-%m-%d").date()
        self.assertEqual(date_to_str(date_object), '2014-11-27')


class GenerateWeekTest(TestCase):

    def test_generate_week_with_date_ending_should_return_ascending_dates_list(self):
        dates = generate_one_week_date('2014-11-11')
        self.assertEqual(dates[0].strftime("%Y-%m-%d"), '2014-11-05')
        self.assertEqual(dates[1].strftime("%Y-%m-%d"), '2014-11-06')
        self.assertEqual(dates[2].strftime("%Y-%m-%d"), '2014-11-07')
        self.assertEqual(dates[3].strftime("%Y-%m-%d"), '2014-11-08')
        self.assertEqual(dates[4].strftime("%Y-%m-%d"), '2014-11-09')
        self.assertEqual(dates[5].strftime("%Y-%m-%d"), '2014-11-10')
        self.assertEqual(dates[6].strftime("%Y-%m-%d"), '2014-11-11')

    def test_generate_week_with_date_ending_should_work_across_months(self):
        dates = generate_one_week_date('2014-11-03')
        self.assertEqual(dates[0].strftime("%Y-%m-%d"), '2014-10-28')
        self.assertEqual(dates[1].strftime("%Y-%m-%d"), '2014-10-29')
        self.assertEqual(dates[2].strftime("%Y-%m-%d"), '2014-10-30')
        self.assertEqual(dates[3].strftime("%Y-%m-%d"), '2014-10-31')
        self.assertEqual(dates[4].strftime("%Y-%m-%d"), '2014-11-01')
        self.assertEqual(dates[5].strftime("%Y-%m-%d"), '2014-11-02')
        self.assertEqual(dates[6].strftime("%Y-%m-%d"), '2014-11-03')

    def test_get_day_name_from_date(self):
        date = datetime.date(2014, 11, 26)
        self.assertEqual(date_to_dayname(date), 'Wednesday')
