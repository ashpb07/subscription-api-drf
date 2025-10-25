from django.db import models

# Create your models here.
class Userinfo(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField( max_length=254)
    pass1=models.CharField(max_length=25)
    pass1=models.CharField(max_length=25)
