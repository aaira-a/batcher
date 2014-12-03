from django.http import HttpResponseNotFound
from django.shortcuts import render
from batch_apps.models import App, Execution
from batch_apps.generator import *


def today():
    return get_current_date_in_gmt8()


def index(request):
    return specific_date(request, date_to_str(today()))


def specific_date(request, yyyy_mm_dd):
    date_ = date_from_str(yyyy_mm_dd)

    if date_ > today():
        return HttpResponseNotFound("<h1>Page not found - Can not show date more than today</h1>")

    else:
        executions_list = Execution.objects.generate_and_return_active_apps_execution_objects(date_)
        context = {'date': date_, 'executions_list': executions_list}
        return render(request, 'executions.html', context)


def one_week_view(request, yyyy_mm_dd):
    date_ = date_from_str(yyyy_mm_dd)

    if date_ > today():
        return HttpResponseNotFound("<h1>Page not found - Can not show date more than today</h1>")

    else:
        execution_matrix = construct_weekly_execution_matrix(date_)
        dates = generate_one_week_date(date_)
        context = {'dates': dates, 'execution_matrix': execution_matrix}
        return render(request, 'executions_week.html', context)


def construct_weekly_execution_matrix(date_):
    execution_matrix = []

    dates = generate_one_week_date(date_)
    for date in dates:
        Execution.objects.generate_and_return_active_apps_execution_objects(date)

    active_apps = App.objects.filter(is_active=True)
    for app in active_apps:
        app_executions_for_a_week = []

        for date in dates:
            app_executions_for_a_week.append(Execution.objects.filter(app=app, day__date=date))

        execution_matrix.append(app_executions_for_a_week)

    return execution_matrix
