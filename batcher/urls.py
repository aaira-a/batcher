from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^executions/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', 'batch_apps.views.specific_date', name='exec_date'),    
    url(r'^executions/$', 'batch_apps.views.index', name='exec'),
)
