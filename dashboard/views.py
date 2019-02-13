from django.shortcuts import render
import datetime
from django.utils import timezone
from .models import destination,package

# Create your views here.

def dashboard(request):
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
		articles = destination.objects.all().filter(d_category__icontains=search_text)
		return render(request,'dashboard/filter.html',{'articles':articles})

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
	g = package.objects.all().get(id=pk)
	return render(request, 'dashboard/destination-item.html',{'f':f, 'g':g},locals())