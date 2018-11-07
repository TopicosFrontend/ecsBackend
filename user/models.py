from django.db import models
from collector.models import CollectorInfo

class Code(models.Model):
    cfn = models.CharField(max_length=13)
    ecn = models.CharField(max_length=12)
    in_use = models.BooleanField(default=True)
    collector = models.ForeignKey(CollectorInfo, on_delete=models.CASCADE)

class Form(models.Model):
    code = models.OneToOneField(Code, on_delete=models.CASCADE)

class Section(models.Model):
    title = models.CharField(max_length=30)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

class Item(models.Model):
    question = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
