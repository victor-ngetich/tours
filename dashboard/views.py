from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from .models import destination,package, booking
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
	a = booking.objects.all().filter(username=request.user)
	return render(request, 'dashboard/bookings.html', {'a':a},locals())

def payments(request):
    return render(request, 'dashboard/payments.html')

def addpackage(request):
    return render(request, 'dashboard/pages/add-package.html')

def bookpackage(request, pk): 
	if request.method == 'POST':
		name = request.POST['name']
		p = package.objects.get(pk=pk)
		b = booking.objects.create(t_number=name,p_name=p, username=request.user, p_price=p.p_price)
		return HttpResponseRedirect('/dashboard/bookings/')
	else:
		return HttpResponseRedirect('/')