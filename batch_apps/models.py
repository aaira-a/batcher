from django.db import models
from django_mailbox.models import Message

DATE_PATTERNS = (
    ('', ''),
    ('dd/mm/yyyy', 'dd/mm/yyyy'),
    ('mm/dd/yyyy', 'mm/dd/yyyy'),
    ('ddmm/yyyy',  'ddmm/yyyy'),
    ('mmdd/yyyy',  'mmdd/yyyy'),
)

FREQUENCY_CHOICES = (
    ('daily', 'daily'),
    ('weekly - mondays',    'weekly - mondays'),
    ('weekly - tuesdays',   'weekly - tuesdays'),
    ('weekly - wednesdays', 'weekly - wednesdays'),
    ('weekly - thursdays',  'weekly - thursdays'),
    ('weekly - fridays',    'weekly - fridays'),
    ('weekly - saturdays',  'weekly - saturdays'),
    ('weekly - sundays',    'weekly - sundays'),
    ('monthly - day 01',   'monthly - day 01'),
)

COUNTRY_CHOICES = (
    ('MY', 'MY'),
    ('SG', 'SG'),
)

APP_CATEGORY_CHOICES = (
    ('consumer', 'consumer'),
    ('customer', 'customer'),
)


class App(models.Model):

    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    description = models.TextField(max_length=500, default='', blank=True)
    frequency = models.CharField(max_length=64, choices=FREQUENCY_CHOICES, default='', blank=True)
    repo = models.CharField(max_length=128, default='', blank=True)
    country = models.CharField(max_length=16, choices=COUNTRY_CHOICES, default='', blank=True)
    category = models.CharField(max_length=16, choices=APP_CATEGORY_CHOICES, default='', blank=True)

    def __str__(self):
        return self.name


class Pattern(models.Model):

    app = models.ForeignKey(App)
    name_pattern = models.CharField(max_length=128)
    is_capturing_date = models.BooleanField(default=False)
    date_pattern = models.CharField(max_length=64, choices=DATE_PATTERNS, default='', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name_pattern


class Day(models.Model):

    date = models.DateField(unique=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class ExecutionManager(models.Manager):

    def generate_and_return_active_apps_execution_objects(self, date_):
        day = self.get_or_create_day_object(date_)
        active_apps = App.objects.filter(is_active=True)
        executions = self.get_or_create_execution_objects(day, active_apps)
        return executions

    def get_or_create_day_object(self, date_):
        day, is_new = Day.objects.get_or_create(date=date_)
        return day

    def get_or_create_execution_objects(self, day_, applist):
        executions = []

        for app in applist:
            execution = self.get_or_create_execution_object(day_, app)
            executions.append(execution)

        executions_strip_none = [x for x in executions if x is not None]

        return executions_strip_none

    def get_or_create_execution_object(self, day_, app_):
        if app_.is_active is True:
            execution, is_new = Execution.objects.get_or_create(
                                    day=day_,
                                    app=app_,
                                    is_due_today=self.app_due_today(app_, day_.date))
            return execution

        else:
            return None

    def app_due_today(self, app, date_today):
        if app.frequency == 'daily':
            return True

        elif 'weekly' in app.frequency:
            return bool(date_today.strftime("%A") == self.get_day_of_week_from_string(app.frequency))

        elif 'monthly' in app.frequency:
            return bool(date_today.strftime("%d") == self.get_day_of_month_from_string(app.frequency))

        else:
            return False

    def get_day_of_week_from_string(self, weekly_date_string):
        day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for day in day_list:
            if day.lower() in weekly_date_string.lower():
                return day

    def get_day_of_month_from_string(self, monthly_date_string):
        day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                    '21', '22', '23', '24', '25', '26', '27', '18', '20', '30', '31',
                    ]

        for day in day_list:
            if day in monthly_date_string:
                return day


class Execution(models.Model):
    day = models.ForeignKey(Day)
    app = models.ForeignKey(App)
    email = models.ForeignKey(Message, null=True, blank=True)
    is_executed = models.BooleanField(default=False)
    is_due_today = models.BooleanField(default=False)

    objects = ExecutionManager()

    def __str__(self):

        if self.is_executed is True:
            return str(self.app) + " executed on " + str(self.day)

        elif (self.is_executed is False and
              self.is_due_today is True):
            return str(self.app) + " yet to be executed on " + str(self.day)

        else:
            return str(self.app) + " not to be executed on " + str(self.day)
