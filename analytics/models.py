from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)



class Traffic(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status = models.IntegerField()

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    response_time = models.FloatField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)