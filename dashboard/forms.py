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

	class Meta:
		model = package
		fields = ('p_name','p_category','d_name', 'agency_phone', 'pricep_adult', 'pricep_kid', 'from_day', 'to_day', 'p_slots', 'available', 'p_description')
		widgets = {
			'p_name': forms.TextInput(attrs={'class':'form-control'}),
			'p_category': forms.Select(attrs={'class':'form-control'}),
			'd_name': forms.Select(attrs={'class':'form-control'}),
			'agency_phone': forms.TextInput(attrs={'class':'form-control'}),
			'pricep_adult': forms.TextInput(attrs={'class':'form-control'}),
			'pricep_kid': forms.TextInput(attrs={'class':'form-control'}),
            'from_day': DateInput(attrs={'class':'form-control'}),
			'to_day': DateInput(attrs={'class':'form-control'}),
			'p_slots': forms.TextInput(attrs={'class':'form-control'}),
			'p_description': forms.Textarea(attrs={'class':'form-control','name':'description','rows':'10'}),
        }

	def clean_phone(self):
		phone = self.cleaned_data.get("agency_phone")
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
			'p_name': forms.TextInput(attrs={'class':'form-control'}),
			'p_category': forms.Select(attrs={'class':'form-control'}),
			'agency_phone': forms.TextInput(attrs={'class':'form-control'}),
			'pricep_adult': forms.TextInput(attrs={'class':'form-control'}),
			'pricep_kid': forms.TextInput(attrs={'class':'form-control'}),
			'd_name': forms.Select(attrs={'class':'form-control'}),
            'from_day': DateInput(attrs={'class':'form-control'}),
			'to_day': DateInput(attrs={'class':'form-control'}),
			'p_slots': forms.TextInput(attrs={'class':'form-control'}),
			'p_description': forms.Textarea(attrs={'class':'form-control','name':'description','rows':'10'}),
        }

class BookingOptions(forms.ModelForm):

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

class EditProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'email'
		)
		widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
        }
