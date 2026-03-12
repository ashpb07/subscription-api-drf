from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Plan(models.Model):

    name = models.CharField(max_length=100,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    billing_cycle = models.CharField(max_length=50, default="monthly")
    limits = models.JSONField(default=dict)   # {"api_calls": 5000, "storage_mb": 1000}



class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)


class Usage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_calls = models.IntegerField(default=0)
    storage_used_mb = models.IntegerField(default=0)
    last_reset = models.DateTimeField(auto_now_add=True)
