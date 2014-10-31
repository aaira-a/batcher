from batch_apps.models import Day, Execution
import datetime
import pytz


def get_current_date_in_gmt8():
    current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    return current_datetime.date()


def create_day_object(date_):
    day, is_new = Day.objects.get_or_create(date=date_)
    return day


def create_execution_object(day_, app_):

    if app_.is_active is True:
        execution, is_new = Execution.objects.get_or_create(day=day_, app=app_)
        return execution

    else:
        return None
