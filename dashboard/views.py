from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.contrib import messages
from .models import destination, package, booking
from dashboard.forms import AddPackage
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

def explore(request):
	now = datetime.datetime.now()
	d = destination.objects.all()
	# inq= len(Inquiries.objects.all().filter(user_id = request.user))
	# inv = len(services.objects.all().filter(user_id = request.user))
	# inquiries = InquiriesTable(Inquiries.objects.all().filter(user_id = request.user).order_by('-created_at'))
	# RequestConfig(request, paginate={"per_page": 5}).configure(inquiries)
	data = destination.objects.all()
	return render(request, 'dashboard/index.html',{'destination':d,'data':data},locals())

def filter (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = package.objects.all().filter(p_category__icontains=search_text)
		art = package.objects.all().values_list('d_name',flat=True).filter(p_category__icontains=search_text).distinct()
		r = destination.objects.all()
		for i in art:
			r = destination.objects.all().get(d_name__field=i)
			print(r)
		return render(request,'dashboard/filter2.html',{'articles':r,'art':art})

def filter2 (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = destination.objects.all().filter(d_location__icontains=search_text)
		return render(request,'dashboard/filter.html',{'articles':articles})

def filter3 (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = destination.objects.all().filter(d_package_size__icontains=search_text)
		return render(request,'dashboard/filter.html',{'articles':articles})

def test1(request,pk):
	f = destination.objects.all().get(pk=pk)
	g = package.objects.all().filter(d_name=f)
	return render(request, 'dashboard/destination.html',{'f':f,'g':g},locals())

def editprofile(request):
    return render(request, 'dashboard/pages/edit-profile.html')

def bookings1(request):
	a = booking.objects.all().filter(user=request.user)
	return render(request, 'dashboard/bookings.html', {'a':a},locals())

def payments(request):
    return render(request, 'dashboard/payments.html')

def allpackages(request):
	b = request.user.get_full_name()
	a = package.objects.all().filter(p_agency=b)
	return render(request, 'dashboard/a-packages.html', {'a':a},locals())

@csrf_protect
@ensure_csrf_cookie
def editpackage(request, pk):
	if request.method == 'POST':
		b = request.user.get_full_name()
		instance = package.objects.get(pk=pk)

		form = AddPackage(initial={'Package Name': instance.p_name})
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('dashboard/editpackage/')
	else:
		form = AddPackage()
	return render(request, 'dashboard/pages/edit-package.html', {'form':form})

def payments1(request):
    return render(request, 'dashboard/a-payments.html')

def editprofile1(request):
    return render(request, 'dashboard/pages/a-edit-profile.html')

def bookpackage(request, pk): 
	if request.method == 'POST':
		name = request.POST['name']
		p = package.objects.get(pk=pk)
		b = booking.objects.create(t_number=name,packages=p, user=request.user, p_price=p.p_price, d_name=p.d_name)
		# b.packages.set(p)
		return HttpResponseRedirect('/dashboard/bookings/')
	else:
		return HttpResponseRedirect('/')

@csrf_protect
@ensure_csrf_cookie
def post(request):
	b = request.user.get_full_name()
	if request.method=="POST":
		form = AddPackage(request.POST or None)

		if form.is_valid():
			name = form.cleaned_data['p_name']
			category = form.cleaned_data['p_category']
			destination = form.cleaned_data['d_name']
			phone = form.cleaned_data['phone']
			price = form.cleaned_data['price']
			payinfo = form.cleaned_data['payment_info']
			duration = form.cleaned_data['duration']
			description = form.cleaned_data['description']

			package.objects.create(p_name=name,p_category=category,d_name=destination,p_agency=b,agency_phone=phone,p_price=price,p_payment_info=payinfo,p_duration=duration,p_description=description)
			return HttpResponseRedirect('/dashboard/allpackages/')
			messages.info(request, 'Your product was posted successfully.')
		else:
			return render(request, 'dashboard/pages/add-package.html',{'form':form})
	else:			
		form = AddPackage()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = AddPackage()
		return render(request, 'dashboard/pages/add-package.html',args)

def delete_bookings(request, pk=None):

    item= get_object_or_404(booking, pk=pk)

    creator= item.user.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        item.delete()
        messages.success(request, "Post successfully deleted!")
        return HttpResponseRedirect("/dashboard/bookings/")
    
    context= {'item': item,
              'creator': creator,
              }
    
    return render(request, 'Blog/movies-delete-view.html', context)