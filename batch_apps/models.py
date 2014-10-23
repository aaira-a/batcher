from django.db import models


class App(models.Model):

    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    description = models.TextField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.name


class Pattern(models.Model):

    app = models.ForeignKey(App)
    pattern_string = models.CharField(max_length=500)
    is_capturing_date = models.BooleanField(default=False)
    date_pattern = models.CharField(max_length=500, default='', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.pattern_string


class Day(models.Model):

    date = models.DateField()

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Execution(models.Model):
    day = models.ForeignKey(Day)
    app = models.ForeignKey(App)

    def __str__(self):
        return str(self.day) + " " + str(self.app)
