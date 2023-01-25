#from django.conf.urls import path, include
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path(r'^$', views.activate, name='activate'),    
]
