from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^executions/week/(?P<yyyy_mm_dd>\d{4}-\d{2}-\d{2})/$', 'batch_apps.views.one_week_view', name='weekly_date'),
                       url(r'^executions/week/$', 'batch_apps.views.one_week_view', name='weekly_default'),
                       url(r'^executions/day/(?P<yyyy_mm_dd>\d{4}-\d{2}-\d{2})/$', 'batch_apps.views.specific_date', name='daily_date'),
                       url(r'^executions/day/$', 'batch_apps.views.specific_date', name='daily_default'),
                       url(r'^executions/$', RedirectView.as_view(pattern_name='weekly_default', permanent=False), name='index'),
                       url(r'^$', RedirectView.as_view(pattern_name='index', permanent=False), name='superindex'),
                       url(r'^maintenance/$', 'batch_apps.views.maintenance', name='maintenance'),
                       url(r'^strip$', 'batch_apps.views.strip', name='strip'),
                       url(r'^vacuum$', 'batch_apps.views.vacuum', name='vacuum'),
                       )
