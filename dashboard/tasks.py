from celery import Celery
from celery import task
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User


import time

# logger=get_task_logger(__name__)


@task
def reverse(string):
    return string[::-1]

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y

# This is the decorator which a celery worker uses

# @shared_task
# def celery_task(counter):
#     email = "vicngetichvictor@gmail.com"
#     time.sleep(30)
#     return '{} Done!'.format(counter)