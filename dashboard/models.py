from django.db import models
from dashboard.choices import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html


class destination(models.Model):

    d_name = models.CharField(max_length=255,blank=True)
    d_location = models.CharField(max_length=255,blank=True)
    d_description = models.TextField(blank=True)
    d_pics = models.FileField(upload_to='dashboard/', max_length=255,blank=True)
    d_days = models.DateField(blank=True,default="2019-01-01")
    d_phone = models.CharField(max_length=15,blank=True)
    d_email = models.EmailField(blank=True)

    def __str__(self):
        return self.d_name

    class Meta:
        ordering = ('d_name',)

class package(models.Model):


    p_name = models.CharField(max_length=255,blank=True)
    p_category = models.CharField(max_length=255, choices=MAYBECHOICE,blank=True)
    d_name = models.ForeignKey(destination, on_delete=models.CASCADE)
    p_agency = models.CharField(max_length=255,blank=True)
    agency_phone = models.IntegerField(blank=True,default=1)
    p_price = models.IntegerField(blank=True,default=0)
    p_payment_info = models.CharField(max_length=255,blank=True)
    p_duration = models.CharField(max_length=255,blank=True)
    p_description = models.CharField(max_length=255,blank=True)
    p_reviews = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.p_name

class booking(models.Model):
    packages = models.ForeignKey(package, on_delete=models.CASCADE)
    d_name = models.CharField(max_length=255,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    p_price = models.IntegerField(blank=True,default=0)
    t_number = models.IntegerField(blank=True,default=1)

    @property
    def total_price(self):
        return self.p_price * self.t_number