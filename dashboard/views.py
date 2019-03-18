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
from django.forms import modelformset_factory
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse
from .models import destination, package, booking, Hotel
from django.db.models import Q
from dashboard.forms import AddPackage, EditPackage, BookingOptions
from paypal.standard.forms import PayPalPaymentsForm
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

def indexsearch (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = destination.objects.all().filter(Q(d_name__icontains=search_text) | Q(d_location__icontains=search_text)| Q(d_phone__icontains=search_text))[:15]
		return render(request,'dashboard/isearch.html',{'articles':articles})
	else:
		search_text = ''
		pass
	
def packagesearch (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = package.objects.all().filter(Q(p_name__icontains=search_text)| Q(p_category__icontains=search_text) | Q(p_agency__icontains=search_text))[:15]
		return render(request,'dashboard/psearch.html',{'articles':articles})
	else:
		search_text = ''
		pass

def ourpackagesearch (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		b = request.user.get_full_name()
		a = package.objects.all().filter(p_agency=b)
		articles = a.filter(Q(p_name__icontains=search_text)| Q(p_category__icontains=search_text) | Q(p_agency__icontains=search_text))[:15]
		return render(request,'dashboard/psearch.html',{'articles':articles})
	else:
		search_text = ''
		pass

def filter3 (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = destination.objects.all().filter(d_package_size__icontains=search_text)
		return render(request,'dashboard/filter.html',{'articles':articles})


def test1(request,pk):
	f = destination.objects.all().get(pk=pk)
	g = package.objects.all().filter(d_name=f)
	h = Hotel.objects.all().filter(destination=f)
	instance = get_object_or_404(destination, id=pk)

# ---Form Start---
	if request.method == 'POST':
		form = BookingOptions(request.POST or None, instance=instance)
		if form.is_valid():
			product = form.save(commit=False)
			product.save()

		return HttpResponseRedirect('/')
	else:
		form = BookingOptions(instance=instance)

# ---Formset Start---
	# HotelFormSet = modelformset_factory(Hotel, fields=('h_name',))
	# if request.method == "POST":
	# 	formset = HotelFormSet(
    #     request.POST,
    #     queryset=Hotel.objects.filter(destination=instance),
    #     )
	# 	if formset.is_valid():
	# 		formset.save()
    #         # Do something.
	# else:
	# 		formset = HotelFormSet(queryset=Hotel.objects.filter(destination=instance))
	# return render(request, 'dashboard/destination.html', {'f':f,'g':g, 'h':h,'instance':instance,'formset': formset})	
# ---Formset End---

	return render(request, 'dashboard/destination.html',{'f':f,'g':g, 'h':h,'instance':instance, 'form': form},locals())

def editprofile(request):
    return render(request, 'dashboard/pages/edit-profile.html')

def bookings1(request):
	a = booking.objects.all().filter(user=request.user)
	# paypal_dict = {
    #     "business": "vicngetichvictor@gmail.com",
    #     "amount": "100.00",
	# 	"currency_code": "USD",
    #     "item_name": "name of the item",
    #     "invoice": "unique-invoice-id",
    #     "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    #     "return": request.build_absolute_uri(reverse('paydone')),
    #     "cancel_return": request.build_absolute_uri(reverse('paycancel')),
    #     "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    # }
	# form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"a": a}
	return render(request, 'dashboard/bookings.html', context, locals())

def payments(request):
    return render(request, 'dashboard/payments.html')

def ourpackages(request):
	b = request.user.get_full_name()
	a = package.objects.all().filter(agency=request.user)
	return render(request, 'dashboard/a-packages.html', {'a':a},locals())

def allpackages(request):
	b = request.user.get_full_name()
	a = package.objects.all()
	e = Hotel.objects.all()
	print(e)
	# instance = get_object_or_404(destination, id=pk)

	if request.method == 'POST':
		form = BookingOptions(request.POST or None)
		if form.is_valid():
			product = form.save(commit=False)
			product.save()

		return HttpResponseRedirect('/')
	else:
		form = BookingOptions()

	return render(request, 'dashboard/allpackages.html', {'a':a, 'e':e, 'form':form},locals())

def allpackages1(request):
	b = request.user.get_full_name()
	a = package.objects.all()
	return render(request, 'dashboard/a-allpackages.html', {'a':a},locals())


# class PackageUpdate(UpdateView):
#     # model = package
#     # fields = ['p_name', 'p_category', 'd_name','p_agency', 'agency_phone', 'pricep_adult','pricep_kid', 'p_payment_info', 'from_day', 'to_day', 'p_description']
#     template_name = 'dashboard/editt-package.html'
#     form_class = EditPackage
#     success_url = '/ourpackages/'

#     def get_object(self):
#         rr = self.kwargs.get("pk")
#         return get_object_or_404(package, pk=rr)

#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

@csrf_protect
@ensure_csrf_cookie
def editpackage (request, pk=None):
	instance = get_object_or_404 (package, pk=pk)
	if request.method=="POST":

		form = EditPackage(request.POST or None, instance=instance)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.info(request, 'Your product was updated successfully.')
			return HttpResponseRedirect('/ourpackages/')
			
		else:
			return render(request, 'dashboard/editt-package.html',{'form':form})


	else:
		form = EditPackage(request.POST or None, instance=instance)

	context = {
		"instance": instance,
		"form": form,
	}
	return render(request, "dashboard/editt-package.html", context)


class BookingDelete(DeleteView):
    model = booking
    success_url = reverse_lazy('bookings1')
	
class PackageDelete(DeleteView):
    model = package
    success_url = reverse_lazy('ourpackages')

def payments1(request):
    return render(request, 'dashboard/a-payments.html')

def editprofile1(request):
    return render(request, 'dashboard/pages/a-edit-profile.html')

def bookpackage(request, pk): 
	if request.method == 'POST':
		form = BookingOptions(request.POST or None)
		try:
			adults = request.POST['name1']
			kids = request.POST['name2']
			start = request.POST['name3']
			end = request.POST['name4']
			hotel = request.POST['name7']
			h = Hotel.objects.get(pk=hotel)
			ph = Hotel.objects.values_list('pricep_adult', flat=True).get(pk=hotel)
			# print(ph)
			#q = destination.objects.all().get(id=pk)
			# q = get_object_or_404(destination, pk=pk)
			price = int(adults)*int(ph)
			# print(price)
			p = package.objects.get(pk=pk)
			d = package.objects.values_list('d_name',flat=True).get(pk=pk)
			a = package.objects.values_list('p_slots',flat=True).get(pk=pk)
			c = int(adults)+int(kids)
			d = int(a)-int(c)
			if d < 0:
				messages.info(request,'The total number of people in your booking exceeds the total number of slots available.')
				return redirect ('test1', pk=d)
			else:
			#v = destination.objects.all().get(id=pk)
			# r = Hotel.objects.get(pk=hotel)

				b = booking.objects.create(user=request.user,hotel=h, agency=p.agency, p_name2=p, d_name=p.d_name, adults=adults,kids=kids, pricep_adult=p.pricep_adult, pricep_kid=p.pricep_kid, start_date=start, end_date=end, pricep_day=p.pricep_day)


				p.p_slots = int(a)-int(c)
				p.save()

				return HttpResponseRedirect('/dashboard/bookings/')
		except:
			messages.info(request,'There must have been a problem, please try again')
			return HttpResponseRedirect('/dashboard/bookings/')
		# if form.is_valid():
		# 	adults = form.cleaned_data['adults']
		# 	kids = form.cleaned_data['kids']
		# 	start = form.cleaned_data['start_date']
		# 	end = form.cleaned_data['end_date']

		# name = request.POST['name']
		
	else:
		form = BookingOptions(request.POST or None)
		return render(request, 'dashboard/bookings.html', {'p':p, 'form':form, 'b':b},locals())

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
			price1 = form.cleaned_data['adult_price']
			price2 = form.cleaned_data['kid_price']
			payinfo = form.cleaned_data['payment_info']
			from_date = form.cleaned_data['from_date']
			to_date = form.cleaned_data['to_date']
			slots = form.cleaned_data['slots']
			description = form.cleaned_data['description']

			package.objects.create(p_name=name,p_category=category,d_name=destination,p_agency=b,agency_phone=phone,pricep_adult=price1, pricep_kid=price2, p_payment_info=payinfo, from_day=from_date, to_day=to_date,p_slots=slots,p_description=description)
			return HttpResponseRedirect('/ourpackages/')
			messages.info(request, 'Your product was posted successfully.')
		else:
			return render(request, 'dashboard/pages/add-package.html',{'form':form})
	else:			
		form = AddPackage()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = AddPackage()
		return render(request, 'dashboard/pages/add-package.html',args)

def delete_bookings1(request, pk=None):

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

def delete_booking(request, pk):
	pp = get_object_or_404(booking, pk=pk)
    # p = booking.objects.get(pk=pk)
	# try:
	if request.method == 'POST':
		pp.delete()
		messages.success(request, "Successfully Deleted")
	else:
		messages.success(request, "Not Deleted")
	# except Exception as e:
	# 	messages.warning(request, "Not Deleted at all: Error{}".format(e))
	context= {'pp': pp,
              }
	return HttpResponseRedirect('/dashboard/bookings/')