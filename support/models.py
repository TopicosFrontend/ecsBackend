from django.db import models

class SupportInfo(models.Model):
    username = models.CharField(max_length=30)
