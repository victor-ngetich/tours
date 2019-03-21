"""tours URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import home, contact, successView
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from accounts.views import (login_view, register_view,logout_page,reset_view,refer_view,success)
from dashboard.views import (explore, filter, filter2, filter3, delete_bookings2, delete_account, indexsearch, packagesearch, PackageDelete, ourpackagesearch, test1, editprofile, bookings1, payments, bookpackage, ourpackages, allpackages, allpackages1, payments1, editprofile1, post, editpackage)
from payment.views import (payprocess, paydone, paycancel)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('home.urls')),
    url(r'^accounts/login/',login_view,name='login'),
    url(r'^logout/',logout_page,name='logout'),
    url(r'^register/',register_view,name='register'),
    url(r'^reset/',reset_view,name='reset'),
    url(r'^refer/',refer_view,name='refer'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',include('accounts.urls')),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^success/',success,name='success'),
    url(r'^explore/',explore,name='explore'),
    url(r'^d_filter/', filter, name='filter'),
    url(r'^indexsearch/', indexsearch, name='indexsearch'),
    url(r'^packagesearch/', packagesearch, name='packagesearch'),
    url(r'^ourpackagesearch/', ourpackagesearch, name='ourpackagesearch'),
    url(r'^p_filter/', filter2, name='filter2'),
    url(r'^t_filter/', filter3, name='filter3'),
    url(r'^bookpackage/(?P<pk>\w+)/',bookpackage,name='bookpackage'),
    url(r'^destination/(?P<pk>\w+)/',test1,name='test1'),
    url(r'^dashboard/editprofile/',editprofile,name='editprofile'),
    url(r'^payprocess/',payprocess,name='payprocess'),
    url(r'^paydone/',paydone,name='paydone'),
    url(r'^paycancel/',paycancel,name='paycancel'),
    url(r'^this-is-a-very-hard-to-guess-url/', include('paypal.standard.ipn.urls')),
    url(r'^dashboard/bookings/',bookings1,name='bookings1'),
    url(r'^dashboard/payments/',payments,name='payments'),
    url(r'^dashboard/addpackage/',post,name='post'),
    url(r'^ourpackages/',ourpackages,name='ourpackages'),
    url(r'^allpackages/',allpackages,name='allpackages'),
    url(r'^allpackages1/',allpackages1,name='allpackages1'),
    url(r'^dashboard/payments1/',payments1,name='payments1'),
    url(r'^dashboard/editprofile1/',editprofile1,name='editprofile1'),
    url(r'^editpackage/(?P<pk>\w+)/$',editpackage,name='editpackage'),
    url(r'^deletebooking/(?P<pk>\d+)/$', delete_bookings2, name='delete_booking'),
    url(r'^deleteaccount/', delete_account, name='delete_account'),
    url(r'^deletepackage/(?P<pk>\d+)/$', PackageDelete.as_view(), name='delete_package'),
    path('contact/', contact, name='sendemail'),
    path('emailsuccess/', successView, name='emailsuccess'),



   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

