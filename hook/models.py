from django.db import models

# Create your models here.
class event(models.Model):
    time = models.DateTimeField()
    msg = models.CharField(max_length=200)
    cma = models.CharField(max_length=200)