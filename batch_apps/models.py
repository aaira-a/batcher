from django.db import models


class App(models.Model):

    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    description = models.TextField(max_length=500, default='', blank=True)

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

    date = models.DateField()

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Execution(models.Model):
    day = models.ForeignKey(Day)
    app = models.ForeignKey(App)

    def __str__(self):
        return str(self.app) + " executed on " + str(self.day)
