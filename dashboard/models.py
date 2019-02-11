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

    name = models.CharField(max_length=255,blank=True)
    location = models.CharField(max_length=255,blank=True)
    category = models.CharField(max_length=255, choices=MAYBECHOICE,blank=True)
    description = models.CharField(max_length=255,blank=True)
    pics = models.FileField(upload_to='dashboard/', max_length=255,blank=True)
    payment_info = models.CharField(max_length=255,blank=True)
    reviews = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    email = models.EmailField(blank=True)

class packages(models.Model):
    name = models.CharField(max_length=255,blank=True)
    package_price = models.IntegerField(blank=True,default=0)
    package_size = models.IntegerField(blank=True,default=0)
