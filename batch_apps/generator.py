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
        execution, is_new = Execution.objects.get_or_create(day=day_, app=app_, is_due_today=app_due_today(app_, day_.date))
        return execution

    else:
        return None


def create_execution_objects(day_, applist):

    executions = []

    for app in applist:
        execution = create_execution_object(day_, app)
        executions.append(execution)

    executions_strip_none = [x for x in executions if x is not None]

    return executions_strip_none


def app_due_today(app, date):

    if app.frequency == 'daily':
        return True

    elif 'weekly' in app.frequency:
        return date.strftime("%A") == get_day_of_week_from_string(app.frequency)

    elif 'monthly' in app.frequency:
        return date.strftime("%d") == get_day_of_month_from_string(app.frequency)

    else:
        return False


def get_day_of_week_from_string(weekly_date_string):

    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for day in day_list:
        if day.lower() in weekly_date_string.lower():
            return day


def get_day_of_month_from_string(monthly_date_string):

    day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23', '24', '25', '26', '27', '18', '20', '30', '31',
                ]

    for day in day_list:
        if day in monthly_date_string:
            return day
