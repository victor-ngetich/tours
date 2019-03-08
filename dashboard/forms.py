from django import forms
from dashboard.choices import *
from django.forms.models import modelformset_factory
from django.forms import BaseModelFormSet
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from dashboard.models import package, destination, booking, Hotel

class DateInput(forms.DateInput):
	input_type = 'date'

class AddPackage(forms.ModelForm):

	p_name = forms.CharField(label='Package Name:',max_length=200,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	p_category = forms.ChoiceField(label='Categories:', choices = MAYBECHOICE, initial='', widget=forms.Select(), required=True)
	d_name = forms.ModelChoiceField(label='Destination Name:',required=True, queryset=destination.objects.all(), widget=forms.Select(attrs={'class':'hidden'}))
	phone =forms.IntegerField(label="Cellphone:",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	price =forms.IntegerField(label="Price (KSh):",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	payment_info = forms.CharField(label="Payment Information", required =True,max_length=200,widget=forms.TextInput(attrs={'class':'form-control','name':'payment_info'}))	
	# attachment = forms.FileField(label="Images:",required=True,widget=forms.ClearableFileInput(attrs={'class':'form-control','multiple':"true",'name':'attachment'}))
	# location = forms.CharField(label="Location:", required =True,max_length=200,widget=forms.TextInput(attrs={'class':'form-control','name':'location'}))
	from_date = forms.DateField(label='From:', initial=datetime.date.today, required=True,widget=DateInput(attrs={'class':'form-control'}))
	to_date = forms.DateField(label='To:', initial=datetime.date.today, required=True,widget=DateInput(attrs={'class':'form-control'}))
	duration=forms.IntegerField(label="Duration (Days):",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))	
	description = forms.CharField(label="Description:", required=True,max_length=250,widget=forms.Textarea(attrs={'class':'form-control','name':'description','rows':'6'}))

	class Meta:
		model = package
		fields = ('p_name','p_category','d_name','phone', 'price','payment_info', 'from_date', 'to_date', 'duration', 'description')

	def clean_phone(self):
		phone = self.cleaned_data.get("phone")
		if phone=="":
			raise forms.ValidationError("Please enter a valid phone number!")
		return phone

	def save(self, commit=True):
		package = super(AddPackage,self).save(commit=False)
		if commit:
			package.save()
		return package

class BookingOptions(forms.ModelForm):

	# hotel = forms.ModelChoiceField(label='Hotel:',required=True, queryset=Hotel.objects.all(), widget=forms.Select(attrs={'class':'hidden'}))
	# hotel3 = forms.ModelChoiceField(label='Destination Hotel2:',required=True, queryset=Hotel.objects.filter(destination=f), widget=forms.Select(attrs={'class':'hidden'}))
	start_date = forms.DateField(label='From:', initial=datetime.date.today, required=True,widget=DateInput(attrs={'class':'form-control'}))
	end_date = forms.DateField(label='To:', initial=datetime.date.today, required=True,widget=DateInput(attrs={'class':'form-control'}))

	class Meta:
		model = booking
		fields = ('adults','kids', 'start_date', 'end_date')

	# def __init__(self, destination, *args, **kwargs):
	# 	aa = destination.objects.all().get(pk=pk)
	# 	ab = Hotel.objects.all().filter(d_name=aa)

	# 	super(BookingOptions, self).__init__(*args, **kwargs)
	# 	self.hotel3['hotel3'].queryset=destination.objects.filter(d_name=ab)


# class BaseHotelFormSet(BaseModelFormSet):
		def __init__(self, destination, Hotel, *args, **kwargs):

    	# def __init__(self, *args, **kwargs):
        		super(BookingOptions, self).__init__(*args, **kwargs)
        		self.hotel['hotel'].queryset = Hotel.objects.filter(destination=instance)

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = booking
#         fields = ('hotel',)
# HotelFormSet = modelformset_factory(Hotel, fields=('h_name',), formset=BaseHotelFormSet, form=BookingForm)