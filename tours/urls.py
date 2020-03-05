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
from django.urls import path, include, re_path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from accounts import views as aviews
from home import views as hviews
from dashboard import views as dviews
from payment import views as pviews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', aviews.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('home.urls')),
    path('login_success/', aviews.login_success, name='login_success'),
    path('register/',aviews.register,name='register'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',include('accounts.urls'), name='activate'),
    # path('activate/<slug:uidb64>/<slug:token>/', include('accounts.urls'), name='activate'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('success/',aviews.success,name='success'),
    path('explore/',dviews.explore,name='explore'),
    path('d_filter/', dviews.filter, name='filter'),
    path('indexsearch/', dviews.indexsearch, name='indexsearch'),
    path('packagesearch/', dviews.packagesearch, name='packagesearch'),
    path('paymentsearch/', dviews.paymentsearch, name='paymentsearch'),
    path('paymentsearch1/', dviews.paymentsearch1, name='paymentsearch1'),
    path('bookingsearch/', dviews.bookingsearch, name='bookingsearch'),
    path('ourpackagesearch/', dviews.ourpackagesearch, name='ourpackagesearch'),
    path('p_filter/', dviews.filter2, name='filter2'),
    path('t_filter/', dviews.filter3, name='filter3'),
    re_path('bookpackage/(?P<pk>\w+)/',dviews.bookpackage,name='bookpackage'),
    re_path('destination/(?P<pk>\w+)/',dviews.test1,name='test1'),
    path('dashboard/profile/edit/',dviews.editprofile,name='editprofile'),
    path('dashboard/profile/password/',dviews.change_password,name='change_password'),
    path('dashboard/profile1/password/',dviews.change_password1,name='change_password1'),
    path('payprocess/',pviews.payprocess,name='payprocess'),
    path('paydone/',pviews.paydone,name='paydone'),
    path('paycancel/',pviews.paycancel,name='paycancel'),
    path('this-is-a-very-hard-to-guess-url/', include('paypal.standard.ipn.urls')),
    path('dashboard/bookings/',dviews.bookings1,name='bookings1'),
    path('dashboard/pending-bookings/',dviews.pending_bookings,name='pending_bookings'),
    path('dashboard/to-do-trips/',dviews.to_do_trips,name='to_do_trips'),
    path('booked/',dviews.bookings2,name='bookings2'),
    path('approved-bookings/',dviews.approved_bookings,name='approved_bookings'),
    path('dashboard/payments/',dviews.payments,name='payments'),
    path('dashboard/payments-filter/',dviews.payments_filter,name='payments_filter'),
    path('dashboard/payments-filter1/',dviews.payments1_filter,name='payments1_filter'),
    path('dashboard/bookings-filter/',dviews.fildel,name='fildel'),
    path('dashboard/addpackage/',dviews.post,name='post'),
    path('ourpackages/',dviews.ourpackages,name='ourpackages'),
    path('unavailable-packages/',dviews.unavailable_packages,name='unavailable_packages'),
    path('allpackages/',dviews.allpackages,name='allpackages'),
    path('allpackages1/',dviews.allpackages1,name='allpackages1'),
    path('dashboard/payments1/',dviews.payments1,name='payments1'),
    path('dashboard/profile1/edit/',dviews.editprofile1,name='editprofile1'),
    re_path('editpackage/(?P<pk>\w+)/$',dviews.editpackage,name='editpackage'),
    re_path('deletebooking/(?P<pk>\d+)/$', dviews.delete_bookings2, name='delete_booking'),
    re_path('deletebooking2/(?P<pk>\d+)/$', dviews.delete_bookings3, name='delete_booking1'),
    re_path('approve-booking/(?P<pk>\d+)/$', dviews.approve_booking, name='approve_booking'),
    path('deleteaccount/', dviews.delete_account, name='delete_account'),
    re_path('deletepackage/(?P<pk>\d+)/$', dviews.PackageDelete.as_view(), name='delete_package'),
    path('contact/', hviews.contact, name='sendemail'),
    path('emailsuccess/', hviews.successView, name='emailsuccess'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

