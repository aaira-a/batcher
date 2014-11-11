from django.http import HttpResponseNotFound
from django.shortcuts import render
from batch_apps.models import App, Execution
from batch_apps.generator import *
import datetime


def index(request):

    today = get_current_date_in_gmt8().strftime("%Y-%m-%d")
    return specific_date(request, today)


def specific_date(request, yyyy_mm_dd):

    today = get_current_date_in_gmt8()
    date_ = datetime.datetime.strptime(yyyy_mm_dd, "%Y-%m-%d").date()

    if date_ > today:
        return HttpResponseNotFound("<h1>Page not found - Can not show date more than today</h1>")

    else:
        day_object = get_or_create_day_object(date_)

        active_apps = App.objects.filter(is_active=True)
        get_or_create_execution_objects(day_object, active_apps)

        executions_list = Execution.objects.filter(day__date=date_)

        context = {'date': date_, 'executions_list': executions_list}
        return render(request, 'executions.html', context)


def one_week_view(request, yyyy_mm_dd):

    today = get_current_date_in_gmt8()
    date_ = datetime.datetime.strptime(yyyy_mm_dd, "%Y-%m-%d").date()

    if date_ > today:
        return HttpResponseNotFound("<h1>Page not found - Can not show date more than today</h1>")

    else:
        dates = generate_one_week_date(yyyy_mm_dd)

        for date in dates:
            day_object = get_or_create_day_object(date)
            active_apps = App.objects.filter(is_active=True)
            get_or_create_execution_objects(day_object, active_apps)

        executions_list = Execution.objects.filter(day__date=dates[0])

        context = {'dates': dates, 'executions_list': executions_list}
        return render(request, 'executions_week.html', context)
