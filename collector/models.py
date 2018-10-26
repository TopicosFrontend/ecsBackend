from django.db import models

class CollectorInfo(models.Model):
    username = models.CharField(max_length=30)
