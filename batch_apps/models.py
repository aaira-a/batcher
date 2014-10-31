from django.db import models
from django_mailbox.models import Message


class App(models.Model):

    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    description = models.TextField(max_length=500, default='', blank=True)
    frequency = models.CharField(max_length=500, default='daily')

    def __str__(self):
        return self.name


class Pattern(models.Model):

    DATE_PATTERNS = (
        ('', ''),
        ('dd/mm/yyyy', 'dd/mm/yyyy'),
        ('mm/dd/yyyy', 'mm/dd/yyyy'),
        ('ddmm/yyyy',  'ddmm/yyyy'),
        ('mmdd/yyyy',  'mmdd/yyyy'),
    )

    app = models.ForeignKey(App)
    name_pattern = models.CharField(max_length=500)
    is_capturing_date = models.BooleanField(default=False)
    date_pattern = models.CharField(max_length=64, choices=DATE_PATTERNS, default='', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name_pattern


class Day(models.Model):

    date = models.DateField(unique=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Execution(models.Model):
    day = models.ForeignKey(Day)
    app = models.ForeignKey(App)
    email = models.ForeignKey(Message, null=True)
    is_executed = models.BooleanField(default=False)
    is_due_today = models.BooleanField(default=False)

    def __str__(self):

        if self.is_executed is True:
            return str(self.app) + " executed on " + str(self.day)

        elif self.is_executed is False and \
                self.is_due_today is True:
            return str(self.app) + " yet to be executed on " + str(self.day)

        else:
            return str(self.app) + " not to be executed on " + str(self.day)
