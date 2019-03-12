from django import forms
from dashboard.choices import *
from django.forms.models import modelformset_factory
from django.forms import BaseModelFormSet
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class ContactForm(forms.Form):
    Subject = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Write the email subject here'
            }
        )
    )
    email = forms.EmailField(
		label='Your Email Address:',
        max_length=254,
        widget=forms.EmailInput(attrs={'style': 'border-color: green;'})
    )
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'style': 'border-color: orange;'}),
        help_text='Write your message and contact details here'
    )