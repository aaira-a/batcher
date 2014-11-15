import datetime
import pytz


def get_current_date_in_gmt8():
    current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    return current_datetime.date()


def generate_one_week_date(week_ending_date_string):
    dates_backward = []
    dates_backward.append(date_from_str(week_ending_date_string))

    for i in range(1, 7):
        dates_backward.append(dates_backward[0] - datetime.timedelta(days=i))

    return dates_backward[::-1]


def generate_one_week_date_string(week_ending_date_string):
    datestrings = []
    dates = generate_one_week_date(week_ending_date_string)

    for date in dates:
        datestrings.append(date_to_str(date) + "\r" + date_to_dayname(date))
    return datestrings


def date_from_str(yyyy_mm_dd):
    return datetime.datetime.strptime(yyyy_mm_dd, "%Y-%m-%d").date()


def date_to_str(date):
    return date.strftime("%Y-%m-%d")


def date_to_dayname(date):
    return date.strftime("%A")
