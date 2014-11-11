from django.contrib import admin
from batch_apps.models import App, Pattern, Day, Execution
from django.db import models
from django.forms import TextInput


class PatternInline(admin.TabularInline):
    model = Pattern
    extra = 0


class AppAdmin(admin.ModelAdmin):
    actions = ['activate_apps', 'deactivate_apps']
    list_display = ('name', 'is_active', 'frequency', 'country', 'category', )
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['is_active']}),
        (None, {'fields': ['frequency']}),
        (None, {'fields': ['country']}),
        (None, {'fields': ['category']}),
        (None, {'fields': ['repo']}),
        ('Description', {'fields': ['description'], }),
    ]
    inlines = [PatternInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '150'})},
    }

    def activate_apps(self, request, queryset):
        queryset.update(is_active=True)
        return 'activated'
    activate_apps.short_description = "Activate selected Apps"

    def deactivate_apps(self, request, queryset):
        queryset.update(is_active=False)
        return 'deactivated'
    deactivate_apps.short_description = "Deactivate selected Apps"


class ExecutionInline(admin.TabularInline):
    model = Execution
    readonly_fields = ('day', 'app')
    extra = 0


class DayAdmin(admin.ModelAdmin):
    model = Day
    inlines = [ExecutionInline]

admin.site.register(App, AppAdmin)
admin.site.register(Day, DayAdmin)
