from django.contrib import admin
from batch_apps.models import App, Pattern


class PatternInline(admin.StackedInline):
    model = Pattern
    extra = 0


class AppAdmin(admin.ModelAdmin):
    fields = ['name', 'is_active']
    inlines = [PatternInline]

admin.site.register(App, AppAdmin)
