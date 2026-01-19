from django.db import models
from django.contrib.auth.models import User

class EmailVerify(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    email_token=models.CharField(max_length=50)
  