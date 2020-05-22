from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Measurement(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    created_by = models.ForeignKey(
        User, related_name="created_by", on_delete=models.CASCADE, null=False)
