from django.shortcuts import render
from batch_apps.models import App, Execution
from batch_apps.generator import *
import datetime


def index(request):

    date_ = datetime.date(2014, 10, 20)
    day_object = get_or_create_day_object(date_)

    active_apps = App.objects.filter(is_active=True)
    get_or_create_execution_objects(day_object, active_apps)

    executions_list = Execution.objects.filter(day__date=date_)

    context = {'date': date_, 'executions_list': executions_list}
    return render(request, 'executions.html', context)


def specific_date(request, yyyy_mm_dd):

    date_ = datetime.datetime.strptime(yyyy_mm_dd, "%Y-%m-%d").date()
    day_object = get_or_create_day_object(date_)

    active_apps = App.objects.filter(is_active=True)
    get_or_create_execution_objects(day_object, active_apps)

    executions_list = Execution.objects.filter(day__date=date_)

    context = {'date': date_, 'executions_list': executions_list}
    return render(request, 'executions.html', context)
