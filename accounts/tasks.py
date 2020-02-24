from celery import Celery
from celery import task
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


import time

# logger=get_task_logger(__name__)


@task
def reverse(string):
    return string[::-1]

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y

# This is the decorator which a celery worker uses
@shared_task(name="email_task")
def email_task(data):
    use= data.get('user1')
    user=User.objects.get(pk=use)
    email= data.get('email')
    current_site= data.get('current_site')
    message = render_to_string('registration/activate-email.html',{
    'user': user,
    'domain': current_site,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'token': account_activation_token.make_token(user),
    })
    mail_subject = 'Activate your Kenyan Thrill account'
    to_email = email
    email = EmailMessage(mail_subject,message, to=[to_email])
    email.send()

# @shared_task
# def celery_task(counter):
#     email = "vicngetichvictor@gmail.com"
#     time.sleep(30)
#     return '{} Done!'.format(counter)