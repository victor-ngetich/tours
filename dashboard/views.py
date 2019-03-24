from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import datetime
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from .models import destination, package, booking, Hotel, payment
from dashboard.tables import PaymentsTable, ApprovedBookingsTable, AgencyPaymentsTable
from django_tables2 import RequestConfig
from django.db.models import Q
from dashboard.forms import (
	AddPackage,
	EditPackage,
	BookingOptions,
	EditProfileForm
)
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

@login_required
def explore(request):
	now = datetime.datetime.now()
	d = destination.objects.all()
	# inq= len(Inquiries.objects.all().filter(user_id = request.user))
	# inv = len(services.objects.all().filter(user_id = request.user))
	# inquiries = InquiriesTable(Inquiries.objects.all().filter(user_id = request.user).order_by('-created_at'))
	# RequestConfig(request, paginate={"per_page": 5}).configure(inquiries)
	return render(request, 'dashboard/index.html',{'destination':d},locals())

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
		articles = package.objects.all().filter(Q(p_name__icontains=search_text) | Q(p_category__icontains=search_text) | Q(p_agency__icontains=search_text))[:15]
		return render(request,'dashboard/psearch.html',{'articles':articles})
	else:
		search_text = ''
		pass

def paymentsearch (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		print(search_text)
		articles = payment.objects.all().filter(Q(booking__icontains=search_text) | Q(agencyname__icontains=search_text) | Q(transaction_id__icontains=search_text) | Q(hotel__icontains=search_text))[:15]
		return render(request,'dashboard/isearch.html',{'articles':articles})
	else:
		search_text = ''
		pass
	

def ourpackagesearch (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		b = request.user.get_full_name()
		a = package.objects.all().filter(p_agency=b)
		articles = a.filter(Q(p_name__icontains=search_text) | Q(p_category__icontains=search_text) | Q(p_agency__icontains=search_text))[:15]
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
	t = timezone.now()
	s = timezone.now() + timedelta(days=999999)
	g = package.objects.all().filter(d_name=f, available=True, to_day__range=[t,s])

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

def bookings1(request):
	a = booking.objects.all().filter(user=request.user)
	# b = booking.objects.all().filter(approved=False)

	# b = booking.objects.get(pk=pk).approved
	# print(b)
	# c = booking.objects.filter(pk=pk).update(approved=True)
	context = {"a": a}
	return render(request, 'dashboard/bookings.html', context, locals())

def to_do_trips(request):
	a = booking.objects.all().filter(user=request.user, approved=True)
	# b = booking.objects.all().filter(approved=False)

	# b = booking.objects.get(pk=pk).approved
	# print(b)
	# c = booking.objects.filter(pk=pk).update(approved=True)
	context = {"a": a}
	return render(request, 'dashboard/to-do-trips.html', context, locals())

def bookings2(request):
	a = booking.objects.all().filter(agency=request.user, approved=False, paid=False)
	context = {"a": a}
	return render(request, 'dashboard/a-booked.html', context, locals())

def approved_bookings(request):
	now = datetime.datetime.now()
	# a = booking.objects.all().filter(agency=request.user, approved=True,)
	b = ApprovedBookingsTable(booking.objects.all().filter(agency=request.user, approved=True, paid=False).order_by('p_name2'))
	RequestConfig(request, paginate={"per_page": 10}).configure(b)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, b)
		return exporter.response('Approved_Bookings.{}'.format(export_format))
	context = {"now":now, "b": b}
	return render(request, 'dashboard/a-booked-approved.html', context, locals())

def payments(request):
	now = datetime.datetime.now()
	payments = PaymentsTable(payment.objects.all().filter(user_id = request.user).order_by('-date_paid'))
	RequestConfig(request, paginate={"per_page": 10}).configure(payments)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, payments)
		return exporter.response('Payments_Report.{}'.format(export_format))
	return render(request, 'dashboard/payments.html', {'now':now, 'payments':payments})

def payments1(request):
	now = datetime.datetime.now()
	payments = AgencyPaymentsTable(payment.objects.all().filter(agency = request.user).order_by('-date_paid'))
	RequestConfig(request, paginate={"per_page": 10}).configure(payments)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, payments)
		return exporter.response('Customer_Payments_Report.{}'.format(export_format))
	return render(request, 'dashboard/a-payments.html', {'now':now, 'payments':payments})

def ourpackages(request):
	b = request.user.get_full_name()
	t = timezone.now()
	s = timezone.now() + timedelta(days=999999)
	a = package.objects.all().filter(Q(agency=request.user), (Q(available=True) | Q(to_day__range=[s,t])))
	return render(request, 'dashboard/a-packages.html', {'a':a},locals())

def unavailable_packages(request):
	b = request.user.get_full_name()
	t = timezone.now()
	s = timezone.now() - timedelta(days=99999)
	a = package.objects.all().filter(Q(agency=request.user), (Q(available=False) | Q(to_day__range=[s,t])))
	return render(request, 'dashboard/a-unavailable-packages.html', {'a':a},locals())

@login_required
def allpackages(request):
	b = request.user.get_full_name()
	t = timezone.now()
	s = timezone.now() + timedelta(days=999999)
	a = package.objects.all().filter(available=True, to_day__range=[t,s])
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
			a = form.cleaned_data.get('p_slots')
			print(a)
			if a < 1:
				instance.available = False
				# instance.p_slots = a
				# instance.save()
				# print(a)
			else:
				pass
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


# class BookingDelete(DeleteView):
# 	model = booking
# 	success_url = reverse_lazy('bookings1')

def delete_bookings2(request, pk):
	d = booking.objects.values_list('adults',flat=True).get(pk=pk)
	e = booking.objects.values_list('kids',flat=True).get(pk=pk)
	c = d+e
	# print(c)
	a = booking.objects.get(pk=pk).p_name2
	f = package.objects.values_list('p_slots',flat=True).get(pk=a.pk)
	# print(f)
	# print(a.pk)
	c = package.objects.filter(pk=a.pk).update(p_slots=f+c)
	# b = a.values_list('p_slots', flat=True)
	# print(b)

	booking.objects.filter(pk=pk).delete()
	return HttpResponseRedirect('/dashboard/bookings/')

def delete_bookings3(request, pk):
	d = booking.objects.values_list('adults',flat=True).get(pk=pk)
	e = booking.objects.values_list('kids',flat=True).get(pk=pk)
	c = d+e
	# print(c)
	a = booking.objects.get(pk=pk).p_name2
	f = package.objects.values_list('p_slots',flat=True).get(pk=a.pk)
	# print(f)
	# print(a.pk)
	c = package.objects.filter(pk=a.pk).update(p_slots=f+c)
	# b = a.values_list('p_slots', flat=True)
	# print(b)

	booking.objects.filter(pk=pk).delete()
	return HttpResponseRedirect('/booked/')

def delete_account(request):
	a = request.user.get_username()
	print(a)
	b = User.objects.values_list('id',flat=True).get(username=a)
	print(b)
	User.objects.get(id=b).delete()
	return HttpResponseRedirect('/accounts/login/')

class PackageDelete(DeleteView):
    model = package
    success_url = reverse_lazy('ourpackages')

def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/profile/edit')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'dashboard/pages/edit-profile.html', args)

def editprofile1(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/profile1/edit')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'dashboard/pages/a-edit-profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/dashboard/editprofile')
        else:
            return redirect('dashboard/profile/password/')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'dashboard/pages/change-password.html', args)

def change_password1(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/dashboard/editprofile1')
        else:
            return redirect('dashboard/profile1/password/')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'dashboard/pages/a-change-password.html', args)

def bookpackage(request, pk): 
	if request.method == 'POST':
		form = BookingOptions(request.POST or None)
		e = request.user.get_full_name()
		f = request.user.email
		# try:
		adults = request.POST['name1']
		kids = request.POST['name2']
		start = request.POST['name3']
		end = request.POST['name4']
		# g = package.objects.values_list('to_day',flat=True).get(pk=pk)
		# h = to_day__range=[t,s]
		# now = date.today()
		# print(d)
		# nows = d - now
		# print(now)
		# s = datetime.datetime.strptime(start, "%Y-%m-%d").date()
		# # t = datetime.datetime.strptime(end, "%m-%d-%Y").date()
		# f = s - now
		# print(f)
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
			messages.info(request,'The total number of people in your booking exceeds the number of slots available.')
			return HttpResponseRedirect('/dashboard/bookings/')
			# return redirect ('test1', pk=d)
		else:
		#v = destination.objects.all().get(id=pk)
		# r = Hotel.objects.get(pk=hotel)

			b = booking.objects.create(user=request.user, user_full=e, clientemail=f, hotel=h, agency=p.agency, agencyname=p.p_agency, agencycontact=p.agency_phone, p_name2=p, d_name=p.d_name, adults=adults,kids=kids, pricep_adult=p.pricep_adult, pricep_kid=p.pricep_kid, start_date=start, end_date=end)
			
			p.p_slots = int(a)-int(c)
			p.save()
			if d < 1:
				# These two lines work too
				# p.available = False
				# p.save()
				e = package.objects.filter(pk=pk).update(available=False)
			else:
				pass
			return HttpResponseRedirect('/dashboard/bookings/')
	# except:
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

def approve_booking(request, pk):
	a = booking.objects.get(pk=pk).approved
	b = booking.objects.filter(pk=pk).update(approved=True)
	return HttpResponseRedirect('/booked/')


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
			phone = form.cleaned_data['agency_phone']
			price1 = form.cleaned_data['pricep_adult']
			price2 = form.cleaned_data['pricep_kid']
			from_date = form.cleaned_data['from_day']
			to_date = form.cleaned_data['to_day']
			slots = form.cleaned_data['p_slots']
			a = form.cleaned_data['available']
			description = form.cleaned_data['p_description']

			if slots < 1:
				a = False
			else:
				pass

			package.objects.create(p_name=name,p_category=category,d_name=destination,p_agency=b,agency_phone=phone,pricep_adult=price1, pricep_kid=price2, from_day=from_date, to_day=to_date,p_slots=slots, available=a, p_description=description)
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