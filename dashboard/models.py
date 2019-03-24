from django.db import models
from dashboard.choices import *
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.utils.html import format_html


class destination(models.Model):

    d_name = models.CharField("Destination", max_length=255,blank=True)
    d_location = models.CharField("Location", max_length=255,blank=True)
    d_description = models.TextField("Description", blank=True)
    d_pic1 = models.FileField("Pic 1", upload_to='dashboard/', blank=True)
    d_pic2= models.FileField("Pic 2", upload_to='dashboard/', blank=True)
    d_pic3 = models.FileField("Pic 3", upload_to='dashboard/', blank=True)
    d_phone = models.CharField("Phone", max_length=15,blank=True)
    d_email = models.EmailField("Email", blank=True)
    d_reviews = models.CharField("Reviews", max_length=255,blank=True)
    d_uploaded_at = models.DateTimeField("Date Added", auto_now_add=True)

    def __str__(self):
        return self.d_name

    class Meta:
        ordering = ('d_name',)

class Hotel(models.Model):
    h_name = models.CharField("Hotel", max_length=255,blank=True)
    destination = models.ForeignKey(destination, on_delete=models.CASCADE, verbose_name="Destination",)
    pricep_adult = models.FloatField("Price per Adult", blank=True,default=0)
    pricep_kid = models.FloatField("Price per Kid", blank=True,default=0)

    def __str__(self):
        return self.h_name

# class DestinationImage(models.Model):
#     destination = models.ForeignKey(destination, on_delete=models.CASCADE, related_name='images')
#     image = models.FileField("Image", upload_to="dashboard/")
#     uploaded_at = models.DateTimeField("Date Added", auto_now_add=True)

def one_month_from_today():
    return timezone.now() + timedelta(days=5)

class package(models.Model):

    p_name = models.CharField("Package Name", max_length=255,blank=True)
    p_category = models.CharField("Category", max_length=255, choices=MAYBECHOICE,blank=True)
    d_name = models.ForeignKey(destination, on_delete=models.CASCADE, verbose_name="Destination",)
    p_agency = models.CharField("Travel Agency", max_length=255,blank=True)
    agency = models.ForeignKey(User, on_delete=models.CASCADE, default=12, verbose_name="Agency",)
    agency_phone = models.CharField("Phone", max_length=10, blank=True)
    pricep_adult = models.FloatField("Price per Adult", blank=True,default=0)
    pricep_kid = models.FloatField("Price per Kid", blank=True,default=0)
    p_description = models.TextField("Description", blank=True)
    from_day = models.DateField("From", default=date.today,blank=True, null=True)
    to_day = models.DateField("To", default=one_month_from_today,blank=True, null=True)
    p_slots = models.IntegerField("Number Slots", blank=True,default=0)
    available = models.BooleanField("Available?", default=True)

    def __str__(self):
        return self.p_name

    class Meta:
        ordering = ('p_name', 'd_name')


def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")

class booking(models.Model):

    p_name2 = models.ForeignKey(package, on_delete=models.CASCADE, verbose_name="Package",)
    d_name = models.CharField("Destination", max_length=255,blank=True)
    agency = models.CharField("Agency", max_length=255,blank=True)
    agencyname = models.CharField("Travel Agency", max_length=255,blank=True)
    agencycontact = models.CharField("Agency Contact", max_length=255,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client",)
    user_full = models.CharField("Client", max_length=255,blank=True)
    clientemail = models.CharField("Client's Email", max_length=255,blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name="Hotel",)
    adults = models.IntegerField("Adults", blank=True,default=1)
    kids = models.IntegerField("Kids", blank=True,default=0)
    pricep_adult = models.FloatField("Price per Adult", blank=True,default=0)
    pricep_kid = models.FloatField("Price per Kid", blank=True,default=0)
    days = models.IntegerField("Days", blank=True,default=1)
    start_date = models.DateField("From", default=date.today,blank=True, null=True, validators=[validate_date])
    end_date = models.DateField("To", default=date.today,blank=True, null=True)
    approved = models.BooleanField("Approved?", default=False)
    paid = models.BooleanField("Paid?", default=False)
    date_added = models.DateTimeField("Date Booked", auto_now_add=True)


    def __str__(self):
        return self.p_name2.p_name

    # def __str__(self):
    #     return '%s - %s' % (self.user, self.p_name2.p_name)

    @property
    def get_total_price(self):
        a = self.pricep_adult * self.adults
        b = self.pricep_kid * self.kids
        c = ((self.end_date - self.start_date).days) + 1
        # d = (c * self.pricep_day)
        return ((a) + (b)) * c

    @property
    def get_usd_price(self):
        e = self.pricep_adult * self.adults
        f = self.pricep_kid * self.kids
        g = ((self.end_date - self.start_date).days) + 1
        # d = (c * self.pricep_day)
        h = ((e) + (f)) * g
        return h * 0.0099

    @property
    def get_total_days(self):
        a = ((self.end_date - self.start_date).days) + 1
        return a

    class Meta:
        ordering = ('-date_added',)

class payment(models.Model):

    booking = models.ForeignKey(booking, on_delete=models.CASCADE, verbose_name="Package",)
    agency = models.CharField("Agency", max_length=255,blank=True)
    agencyname = models.CharField("Travel Agency", max_length=255,blank=True)
    agencycontact = models.CharField("Agency Contact", max_length=255,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client",)
    user_full = models.CharField("Client", max_length=255,blank=True)
    clientemail = models.CharField("Email", max_length=255,blank=True)
    amountpaid = models.FloatField("Amount Paid ($USD)", blank=True,default=0)
    transaction_status = models.CharField("Transaction Status", max_length=255,blank=True)
    transaction_id = models.CharField("Transaction ID", max_length=255,blank=True,unique=True)
    hotel = models.CharField("Preferred Hotel", max_length=255,blank=True)
    adults = models.IntegerField("Adults", blank=True,default=1)
    kids = models.IntegerField("Kids", blank=True,default=0)
    pricep_adult = models.FloatField("Price per Adult", blank=True,default=0)
    pricep_kid = models.FloatField("Price per Kid", blank=True,default=0)
    days = models.IntegerField("Days", blank=True,default=1)
    start_date = models.DateField("From", blank=True, null=True)
    end_date = models.DateField("To", blank=True, null=True)
    date_added = models.DateTimeField("Date Booked", blank=True)
    date_paid = models.DateTimeField("Date Paid", auto_now_add=True)


    # def __str__(self):
    #     return self.booking.p_name2.p_name

    def __str__(self):
        return '%s - %s' % (self.user, self.booking.p_name2.p_name)
