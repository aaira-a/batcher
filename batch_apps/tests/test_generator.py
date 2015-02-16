from django.test import TestCase

from batch_apps.generator import (
    date_from_str,
    date_to_str,
    generate_one_week_date,
    get_current_date_in_gmt8,
)

import pytz
import datetime


class GenerateDateTest(TestCase):

    def test_get_current_date_in_gmt8(self):
        datetime_utc = datetime.datetime.now(pytz.utc)
        converted_datetime = datetime_utc.astimezone((pytz.timezone('Asia/Kuala_Lumpur')))
        self.assertEqual(get_current_date_in_gmt8(), converted_datetime.date())

    def test_date_from_str_should_return_date_object_from_iso_format_string(self):
        expected_date_object = datetime.datetime.strptime('2014-11-25', "%Y-%m-%d").date()
        self.assertEqual(date_from_str('2014-11-25'), expected_date_object)

    def test_date_to_str_should_return_iso_format_string_from_date_object(self):
        date_object = datetime.datetime.strptime('2014-11-27', "%Y-%m-%d").date()
        self.assertEqual(date_to_str(date_object), '2014-11-27')


class GenerateWeekTest(TestCase):

    def test_generate_week_with_date_ending_should_return_ascending_dates_list(self):
        dates = generate_one_week_date(datetime.date(2014, 11, 11))
        expected_datestrings = ['2014-11-05', '2014-11-06', '2014-11-07', '2014-11-08',
                                '2014-11-09', '2014-11-10', '2014-11-11']

        for i in range(len(dates)):
            self.assertEqual(dates[i].strftime("%Y-%m-%d"), expected_datestrings[i])

    def test_generate_week_with_date_ending_should_work_across_months(self):
        dates = generate_one_week_date(datetime.date(2014, 11, 3))
        expected_datestrings = ['2014-10-28', '2014-10-29', '2014-10-30', '2014-10-31',
                                '2014-11-01', '2014-11-02', '2014-11-03']

        for i in range(len(dates)):
            self.assertEqual(dates[i].strftime("%Y-%m-%d"), expected_datestrings[i])
