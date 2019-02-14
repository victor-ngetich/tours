from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html


class destination(models.Model):
    MAYBECHOICE = (
    ('Beaches', 'Beaches'),
    ('Bike Rides', 'Bike Rides'),
    ('Heritage', 'Heritage'),
    ('Hot Air Ballooning', 'Hot Air Ballooning'),
    ('Museums', 'Museums'),
    ('Resorts', 'Resorts'),
    ('Road Trips', 'Road Trips'),
    ('Scenery', 'Scenery'),
    ('Vacation Rentals', 'Vacation Rentals'),
    ('Wildlife', 'Wildlife'),
   )

    d_name = models.CharField(max_length=255,blank=True)
    d_location = models.CharField(max_length=255,blank=True)
    d_category = models.CharField(max_length=255, choices=MAYBECHOICE,blank=True)
    d_description = models.CharField(max_length=255,blank=True)
    d_pics = models.FileField(upload_to='dashboard/', max_length=255,blank=True)
    d_payment_info = models.CharField(max_length=255,blank=True)
    d_days = models.DateField(blank=True,default="2019-01-01")
    d_reviews = models.CharField(max_length=255,blank=True)
    d_phone = models.CharField(max_length=15,blank=True)
    d_email = models.EmailField(blank=True)

    def __str__(self):
        return self.d_name

    class Meta:
        ordering = ('d_name',)

class package(models.Model):
    p_name = models.CharField(max_length=255,blank=True)
    d_name = models.ForeignKey(destination, on_delete=models.CASCADE)
    p_agent = models.CharField(max_length=255,blank=True)
    p_price = models.IntegerField(blank=True,default=0)
    p_duration = models.CharField(max_length=255,blank=True)
    p_description = models.CharField(max_length=255,blank=True)

