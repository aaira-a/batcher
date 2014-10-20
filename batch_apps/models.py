from django.db import models


class App(models.Model):

    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
