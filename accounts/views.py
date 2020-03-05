# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib.sessions.backends.base import SessionBase
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
	)
from .forms import UserLoginForm,MyRegistrationForm,PasswordResetForm
from accounts.tasks import add, email_task
from celery.result import AsyncResult
# Create your views here.
@csrf_protect
def login_view(request):
	if request.method =='POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username,password=password)
			if user.groups.filter(name='Tourist').exists():
				if user.last_login:
					add.delay(12,20)
					login(request, user)
					if 'next' in request.POST:
						return redirect(request.POST.get('next'))
					else:
						return redirect('/explore/')
				# else:
				# 	login(request, user)
				# 	messages.success(request, 'Hello, '+ request.user.username +' Welcome! Looks like you are logging in for the first time.Let us help you point you in the right direction by starting off with updating your user profile.')
				# 	return redirect('/site/w/edit_info/')
			if user.groups.filter(name='Tour Agency').exists():
				if user.last_login:
					login(request, user)
					return redirect('/ourpackages/')
				# else:
				# 	login(request, user)
				# 	messages.success(request, 'Hello, '+ request.user.username +' Welcome! Looks like you are logging in for the first time.Let us help you point you in the right direction by starting off with updating your user profile.')
				# 	return redirect('/site/edit_info/')
			if user.is_staff==True:
				login(request, user)
				return redirect('/admin/')
		else:
			return render(request,'registration/login.html',{"form":form})

	else:
		form = UserLoginForm()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = UserLoginForm()
		return render(request,'registration/login.html',args)

def login_success(request):
    """
    Redirects users based on their group
    """
    if request.user.groups.filter(name='Tourist').exists():
        return redirect('/explore/')
    else:
	    if request.user.groups.filter(name='Tour Agency').exists():
		    return redirect('/ourpackages/')

@csrf_protect
def register(request):
	if request.method =='POST':
		form = MyRegistrationForm(request.POST)  
		if form.is_valid():
			user = (form.save(commit=False))
			user.is_active = False
			user.save()
			group = form.cleaned_data.get('group')
			user.groups.add(group)
			current_site = get_current_site(request).domain
			email = form.cleaned_data.get('email')
			user1= user.pk
			data= {'email':email, 'current_site':current_site, 'user1':user1}
			email_task.delay(data)
			return redirect('/success/')
			return redirect('Please confirm your email address to complete the registration')
		else:
			return render(request,'registration/signup.html',{"form":form})

	else:
		form = MyRegistrationForm()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = MyRegistrationForm()
		return render(request,'registration/signup.html',args)

def success(request):
	return render(request,'registration/success.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request,'registration/valid.html')
    else:
    	return render(request,'registration/invalid.html')
# @csrf_protect
# def logout_page(request):
	# user = User.objects.get(username=request.user.username)
	# [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
	# logout(request)
	# return redirect('/accounts/login/')
# @csrf_protect
# def forgot_view(request):
# 	return render(request,'registration/forgot-password.html')
# def password_reset(request):
# 	form = PasswordResetForm(request.POST or None)
# 	if form.is_valid():
# 		return render(request,"accounts/referal.html")
# 	else:
# 		return render(request,'registration/password_reset_form.html',{"form":form})
# def refer_view(request):
# 	return render(request, 'accounts/referal.html')