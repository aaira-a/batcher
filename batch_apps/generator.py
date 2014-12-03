import datetime
import pytz


def get_current_date_in_gmt8():
    current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    return current_datetime.date()


def generate_one_week_date(week_ending_date):
    dates_backward = []
    dates_backward.append(week_ending_date)

    for i in range(1, 7):
        dates_backward.append(dates_backward[0] - datetime.timedelta(days=i))

    return dates_backward[::-1]


def date_from_str(yyyy_mm_dd):
    return datetime.datetime.strptime(yyyy_mm_dd, "%Y-%m-%d").date()


def date_to_str(date):
    return date.strftime("%Y-%m-%d")
