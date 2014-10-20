from django.db import models


class App(models.Model):

    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)


class Pattern(models.Model):

    app = models.ForeignKey(App)
    pattern_string = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
