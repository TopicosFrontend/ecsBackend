from django.db import models
from collector.models import CollectorInfo

class Code(models.Model):
    cfn = models.CharField(max_length=13)
    ecn = models.CharField(max_length=12)
    collector = models.ForeignKey(CollectorInfo, on_delete=models.CASCADE)

class Form(models.Model):
    code = models.OneToOneField(Code, on_delete=models.CASCADE)
