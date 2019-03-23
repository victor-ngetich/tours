from django import forms
from dashboard.choices import *
from django.forms.models import modelformset_factory
from django.forms import BaseModelFormSet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
import datetime
from dashboard.models import package, destination, booking, Hotel

class DateInput(forms.DateInput):
	input_type = 'date'

def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value

class AddPackage(forms.ModelForm):

	p_name = forms.CharField(label='Package Name:',max_length=200,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	p_category = forms.ChoiceField(label='Category:', choices = MAYBECHOICE, initial='', widget=forms.Select(), required=True)
	d_name = forms.ModelChoiceField(label='Destination:',required=True, queryset=destination.objects.all(), widget=forms.Select(attrs={'class':'hidden'}))
	phone =forms.IntegerField(label="Agent Phone:",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	adult_price =forms.IntegerField(label="Price per Adult (KSh):",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	kid_price =forms.IntegerField(label="Price per Adult (KSh):",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	# attachment = forms.FileField(label="Images:",required=True,widget=forms.ClearableFileInput(attrs={'class':'form-control','multiple':"true",'name':'attachment'}))
	from_date = forms.DateField(label='From:', initial=datetime.date.today, required=True, validators=[present_or_future_date], widget=DateInput(attrs={'class':'form-control'}))
	to_date = forms.DateField(label='To:', initial=datetime.date.today, required=True,widget=DateInput(attrs={'class':'form-control'}))
	slots=forms.IntegerField(label="Slots Available:",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))	
	description = forms.CharField(label="Description:", required=True,max_length=250,widget=forms.Textarea(attrs={'class':'form-control','name':'description','rows':'6'}))

	class Meta:
		model = package
		fields = ('p_name','p_category','d_name', 'from_day', 'to_day')

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

class EditPackage(forms.ModelForm):
	class Meta:
		model = package
		fields = ('p_name', 'p_category', 'd_name', 'agency_phone', 'pricep_adult','pricep_kid', 'from_day', 'to_day', 'p_slots', 'available', 'p_description')
		widgets = {
            'from_day': DateInput(attrs={'class':'form-control'}),
			'to_day': DateInput(attrs={'class':'form-control'}),
        }

class BookingOptions(forms.ModelForm):

	# hotel = forms.ModelChoiceField(label='Hotel:',required=True, queryset=Hotel.objects.all(), widget=forms.Select(attrs={'class':'hidden'}))
	# hotel3 = forms.ModelChoiceField(label='Destination Hotel2:',required=True, queryset=Hotel.objects.filter(destination=f), widget=forms.Select(attrs={'class':'hidden'}))
	adults =forms.IntegerField(label="Adults:", initial = 1, required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	kids =forms.IntegerField(label="Kids:", initial = 0, required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	start_date = forms.DateField(label='From:', initial=datetime.date.today, required=True, widget=DateInput(attrs={'class':'form-control'}))
	end_date = forms.DateField(label='To:', initial=datetime.date.today, required=True,widget=DateInput(attrs={'class':'form-control'}))

	def clean_date(self):
		start_date = self.cleaned_data['start_date']
		if start_date < datetime.date.today():
			raise forms.ValidationError("The date cannot be in the past!")
		return start_date

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

class EditProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'email'
		)
