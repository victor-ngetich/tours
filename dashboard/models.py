from django.db import models
from dashboard.choices import *
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.utils.html import format_html


class destination(models.Model):

    d_name = models.CharField(max_length=255,blank=True)
    d_location = models.CharField(max_length=255,blank=True)
    d_description = models.TextField(blank=True)
    d_pic1 = models.FileField(upload_to='dashboard/', blank=True)
    d_pic2= models.FileField(upload_to='dashboard/', blank=True)
    d_pic3 = models.FileField(upload_to='dashboard/', blank=True)
    d_phone = models.CharField(max_length=15,blank=True)
    d_email = models.EmailField(blank=True)
    d_uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.d_name

    class Meta:
        ordering = ('d_name',)

class DestinationImage(models.Model):
    destination = models.ForeignKey(destination, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to="dashboard/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

def one_month_from_today():
    return timezone.now() + timedelta(days=30)

class package(models.Model):

    p_name = models.CharField(max_length=255,blank=True)
    p_category = models.CharField(max_length=255, choices=MAYBECHOICE,blank=True)
    d_name = models.ForeignKey(destination, on_delete=models.CASCADE)
    p_agency = models.CharField(max_length=255,blank=True)
    agency_phone = models.IntegerField(blank=True,default=1)
    p_price = models.IntegerField(blank=True,default=0)
    p_payment_info = models.CharField(max_length=255,blank=True)
    p_duration = models.CharField(max_length=255,blank=True)
    p_description = models.TextField(blank=True)
    from_day = models.DateField(default=date.today,blank=True, null=True)
    to_day = models.DateField(default=one_month_from_today,blank=True, null=True)
    p_reviews = models.CharField(max_length=255,blank=True)
    favorite_colors = models.CharField(max_length=255,blank=True)


    def __str__(self):
        return self.p_name

    class Meta:
        ordering = ('p_name', 'd_name')

class booking(models.Model):

    FAVORITE_COLORS_CHOICE = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)
    packages = models.ForeignKey(package, on_delete=models.CASCADE)
    d_name = models.ForeignKey(destination, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    p_price = models.IntegerField(blank=True,default=0)
    t_number = models.IntegerField(blank=True,default=1)
    hotel = models.CharField(max_length=255, choices=FAVORITE_COLORS_CHOICE,blank=True)


    @property
    def total_price(self):
        return self.p_price * self.t_number