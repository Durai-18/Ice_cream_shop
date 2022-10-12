from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class mobiux_userregistration (models.Model):
    user_name =models.CharField(max_length=30)
    first_name =models.CharField(max_length=20)
    last_name =models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    password =models.CharField(max_length=100)
    mobile  =models.IntegerField(max_length=10)
    class Meta:
        db_table='mobiux_userregistration'



    
    
