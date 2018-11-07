from django.db import models

class CollectorInfo(models.Model):
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    cellphone = models.CharField(max_length=15)
