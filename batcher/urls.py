from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^executions/week/(?P<yyyy_mm_dd>\d{4}-\d{2}-\d{2})/$', 'batch_apps.views.one_week_view', name='week'),
    url(r'^executions/(?P<yyyy_mm_dd>\d{4}-\d{2}-\d{2})/$', 'batch_apps.views.specific_date', name='exec_date'),
    url(r'^executions/$', 'batch_apps.views.index', name='exec'),
)
