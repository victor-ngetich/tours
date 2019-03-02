from django import forms
from dashboard.choices import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from dashboard.models import package, destination

class AddPackage(forms.ModelForm):
	p_name = forms.CharField(label='Package Name:',max_length=200,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	p_category = forms.ChoiceField(label='Categories:', choices = MAYBECHOICE, initial='', widget=forms.Select(), required=True)
	d_name = forms.ModelChoiceField(label='Destination Name:',required=True, queryset=destination.objects.all())
	p_agency = forms.CharField(label='Tour Agent:',max_length=200,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.CharField(label="Email:", required = True,max_length=70,widget=forms.TextInput(attrs={'multiple':True,'class':'form-control','name':'email'}))
	phone =forms.IntegerField(label="Cellphone:",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	price =forms.IntegerField(label="Price (KSh):",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	payment_info = forms.CharField(label="Payment Information", required =True,max_length=200,widget=forms.TextInput(attrs={'class':'form-control','name':'payment_info'}))	
	# attachment = forms.FileField(label="Images:",required=True,widget=forms.ClearableFileInput(attrs={'class':'form-control','multiple':"true",'name':'attachment'}))
	# location = forms.CharField(label="Location:", required =True,max_length=200,widget=forms.TextInput(attrs={'class':'form-control','name':'location'}))
	duration=forms.IntegerField(label="Duration (Days):",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))	
	description = forms.CharField(label="Description:", required=True,max_length=250,widget=forms.Textarea(attrs={'class':'form-control','name':'description','rows':'6'}))

	class Meta:
		model = package
		fields = ('p_name','p_category','d_name','p_agency','email','phone', 'price','payment_info', 'duration', 'description')

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