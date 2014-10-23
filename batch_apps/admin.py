from django.contrib import admin
from batch_apps.models import App, Pattern, Day, Execution


class PatternInline(admin.TabularInline):
    model = Pattern
    extra = 0


class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['is_active']}),
        ('Description', {'fields': ['description'], 'classes': ['collapse']}),
    ]
    inlines = [PatternInline]


class ExecutionInline(admin.TabularInline):
    model = Execution
    readonly_fields = ('day', 'app')
    extra = 0


class DayAdmin(admin.ModelAdmin):
    model = Day
    inlines = [ExecutionInline]

admin.site.register(App, AppAdmin)
admin.site.register(Day, DayAdmin)
