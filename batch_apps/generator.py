from batch_apps.models import App, Day, Execution
import datetime
import pytz


def get_current_date_in_gmt8():
    current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
    return current_datetime.date()


def generate_and_return_active_apps_execution_objects(date_):
    day = get_or_create_day_object(date_)
    active_apps = App.objects.filter(is_active=True)
    executions = get_or_create_execution_objects(day, active_apps)
    return executions


def get_or_create_day_object(date_):
    day, is_new = Day.objects.get_or_create(date=date_)
    return day


def get_or_create_execution_objects(day_, applist):

    executions = []

    for app in applist:
        execution = get_or_create_execution_object(day_, app)
        executions.append(execution)

    executions_strip_none = [x for x in executions if x is not None]

    return executions_strip_none


def get_or_create_execution_object(day_, app_):

    if app_.is_active is True:
        execution, is_new = Execution.objects.get_or_create(day=day_, app=app_, is_due_today=app_due_today(app_, day_.date))
        return execution

    else:
        return None


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
