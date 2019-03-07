from django import forms
from dashboard.choices import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from dashboard.models import package, destination, booking

class DateInput(forms.DateInput):
	input_type = 'date'

class AddPackage(forms.ModelForm):

	FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)
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
	favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )

	class Meta:
		model = package
		fields = ('p_name','p_category','d_name','phone', 'price','payment_info', 'from_date', 'to_date', 'duration', 'description', 'favorite_colors')

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
	FAVORITE_COLORS_CHOICE = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)

	hotel = forms.ChoiceField(label='Hotel:', choices = FAVORITE_COLORS_CHOICE, initial='', widget=forms.Select(), required=False)

	class Meta:
		model = booking
		fields = ('hotel',)
