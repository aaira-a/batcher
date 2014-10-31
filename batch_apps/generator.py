from batch_apps.models import Day
import datetime
import pytz


def get_current_date_in_gmt8():
    current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    return current_datetime.date()


def create_day_object(date_):
    day = Day.objects.create(date=date_)
    return day
