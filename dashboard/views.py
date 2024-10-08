from django.shortcuts import render
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import datetime
from datetime import datetime
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
	EditProfileForm,
	# ProfileForm
)
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import get_list_or_404, get_object_or_404
from dashboard.tasks import add
from celery.result import AsyncResult

# Create your views here.

def explore(request):
	now = datetime.now()
	# d = add.delay(12,20)
	# d.id
	# f= d.id
	# print(f)
	# work = AsyncResult(f)
	# if work.ready():                     # check task state: true/false
	# 	try:
	# 		result = work.get()
	# 		return result
	# 	except:
	# 		pass
	# else:
	# 	result = "Not ready"
	# 	return  result
	# print(result)
	d = destination.objects.all()
	# inq= len(Inquiries.objects.all().filter(user_id = request.user))
	# inv = len(services.objects.all().filter(user_id = request.user))
	# inquiries = InquiriesTable(Inquiries.objects.all().filter(user_id = request.user).order_by('-created_at'))
	# RequestConfig(request, paginate={"per_page": 5}).configure(inquiries)
	return render(request, 'dashboard/index.html',{'destination':d})

def filter (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = package.objects.all().filter(p_category__icontains=search_text)
		art = package.objects.all().values_list('d_name',flat=True).filter(p_category__icontains=search_text).distinct()
		r = destination.objects.all()
		for i in art:
			r = destination.objects.all().get(d_name__field=i)
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
		articles = payment.objects.all().filter(Q(user_id = request.user), Q(agencyname__icontains=search_text) | Q(transaction_id__icontains=search_text) | Q(hotel__icontains=search_text) | Q(date_paid__icontains=search_text))[:15]

		now = datetime.now()
		payments = PaymentsTable(articles)
		RequestConfig(request, paginate={"per_page": 5}).configure(payments)

		export_format = request.GET.get('_export', None)
		if TableExport.is_valid_format(export_format):
			exporter = TableExport(export_format, payments)
			return exporter.response('Payments_Report.{}'.format(export_format))

		return render(request,'dashboard/paysearch1.html',{'payments':payments})
	else:
		search_text = ''
		pass

def paymentsearch1 (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = payment.objects.all().filter(Q(agency = request.user), Q(user_full__icontains=search_text)| Q(clientemail__icontains=search_text) | Q(transaction_id__icontains=search_text) | Q(hotel__icontains=search_text) | Q(date_paid__icontains=search_text))[:15]

		now = datetime.now()
		payments = AgencyPaymentsTable(articles)
		RequestConfig(request, paginate={"per_page": 5}).configure(payments)

		export_format = request.GET.get('_export', None)
		if TableExport.is_valid_format(export_format):
			exporter = TableExport(export_format, payments)
			return exporter.response('Customer_Payments_Report.{}'.format(export_format))

		return render(request,'dashboard/paysearch2.html',{'payments':payments})
	else:
		search_text = ''
		pass

def bookingsearch (request):
	if request.method=="POST":
		search_text = request.POST['search_text']
		articles = booking.objects.all().filter(Q(agency=request.user, approved=True, paid=False), Q(user_full__icontains=search_text) | Q(clientemail__icontains=search_text) | Q(date_added__icontains=search_text))[:15]

		now = datetime.now()
		b = ApprovedBookingsTable(articles)
		RequestConfig(request, paginate={"per_page": 5}).configure(b)

		export_format = request.GET.get('_export', None)
		if TableExport.is_valid_format(export_format):
			exporter = TableExport(export_format, b)
			return exporter.response('Approved_Bookings.{}'.format(export_format))

		return render(request,'dashboard/bsearch1.html',{'b':b})
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


@login_required
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

		return redirect('/')
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

	return render(request, 'dashboard/destination.html',{'f':f,'g':g, 'h':h,'instance':instance, 'form': form})

def bookings1(request):
	a = booking.objects.all().filter(user=request.user).order_by('paid', '-approved', '-id')
	# b = booking.objects.all().filter(approved=False)

	# b = booking.objects.get(pk=pk).approved
	# print(b)
	# c = booking.objects.filter(pk=pk).update(approved=True)
	context = {"a": a}
	return render(request, 'dashboard/bookings1.html', context)

def pending_bookings(request):
	a = booking.objects.all().filter(user=request.user, approved=False, paid =False)
	# b = booking.objects.all().filter(approved=False)

	# b = booking.objects.get(pk=pk).approved
	# print(b)
	# c = booking.objects.filter(pk=pk).update(approved=True)
	context = {"a": a}
	return render(request, 'dashboard/pending-bookings.html', context)

@login_required
def to_do_trips(request):
	a = booking.objects.all().filter(user=request.user, approved=True).order_by('-paid', '-id')
	# b = booking.objects.all().filter(approved=False)

	# b = booking.objects.get(pk=pk).approved
	# print(b)
	# c = booking.objects.filter(pk=pk).update(approved=True)
	context = {"a": a}
	return render(request, 'dashboard/to-do-trips.html', context)

def bookings2(request):
	a = booking.objects.all().filter(agency=request.user, approved=False, paid=False)
	context = {"a": a}
	return render(request, 'dashboard/a-booked.html', context)

def approved_bookings(request):
	now = datetime.now()
	# a = booking.objects.all().filter(agency=request.user, approved=True,)
	b = ApprovedBookingsTable(booking.objects.all().filter(agency=request.user, approved=True).order_by('p_name2'))
	RequestConfig(request, paginate={"per_page": 10}).configure(b)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, b)
		return exporter.response('Approved_Bookings.{}'.format(export_format))
	context = {"now":now, "b": b}
	return render(request, 'dashboard/a-booked-approved.html', context)

def deleteabooking(request):
	if request.method=="POST":
		
		
		a = request.POST.getlist('check')
		if bool(a)==True:
			for n in a:
				y = booking.objects.get(pk=n)
				print(n)
				# attach = booking_attach.objects.filter(urlhash=y.urlhash)
				# for i in attach:
				# 	os.remove(i.attachment.path)
				# 	i.delete()
				y.delete()
			messages.info(request, 'Booking deleted!')
			return redirect('/approved-bookings/')
		else:
			messages.info(request, 'No item selected!')
			return redirect('/approved-bookings/')
	else:
		return redirect('/approved-bookings/')

def fildel(request):
	if 'fil' in request.POST:
		# print(request.POST['del'])
		return bookings_filter(request)
	elif 'del' in request.POST:
		# print(request.POST['fil'])
		return deleteabooking(request)
	elif 'expfil' in request.POST:
		# print(request.POST['del'])
		return bookings_filter(request)

def payments(request):
	now = datetime.now()
	payments = PaymentsTable(payment.objects.all().filter(user_id = request.user).order_by('-date_paid'))
	RequestConfig(request, paginate={"per_page": 5}).configure(payments)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, payments)
		return exporter.response('Payments_Report.{}'.format(export_format))
	return render(request, 'dashboard/payments.html', {'now':now, 'payments':payments})

def payments_filter(request):
	if request.method=="POST":
		a = request.POST['start1']
		b = request.POST['end1']
		# f = u''b''
		c = str(datetime(*[int(v) for v in a.replace('T', '-').replace(':', '-').split('-')]))
		d = str(datetime(*[int(v) for v in b.replace('T', '-').replace(':', '-').split('-')]))
		# print(d)
		# s = str(datetime.strptime(c, "%Y-%m-%d %H:%M:%S").date())
		# t = datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date()
		# v = datetime.strptime(c, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S.%f')
		f = datetime.strptime(c, '%Y-%m-%d %H:%M:%S')
		g = f.strftime('%Y-%m-%d %H:%M:%S.%f')

		h = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
		i = h.strftime('%Y-%m-%d %H:%M:%S.%f')
		# dt = datetime.strptime(v, '%Y-%m-%d %H:%M:%S.%f')
		# print(v)
		# e = unicode(v, "utf-8")
		# print(e)


		# print(a)
		# print(b)
	else:
		pass
	now = datetime.now()
	payments = PaymentsTable(payment.objects.all().filter(user_id = request.user, date_paid__range=[g, i]).order_by('-date_paid'))
	RequestConfig(request, paginate={"per_page": 10}).configure(payments)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, payments)
		return exporter.response('Payments_Report.{}'.format(export_format))
	return render(request, 'dashboard/payments.html', {'now':now, 'payments':payments})

def payments1_filter(request):
	if request.method=="POST":
		a = request.POST['start1']
		b = request.POST['end1']

		c = str(datetime(*[int(v) for v in a.replace('T', '-').replace(':', '-').split('-')]))
		d = str(datetime(*[int(v) for v in b.replace('T', '-').replace(':', '-').split('-')]))

		f = datetime.strptime(c, '%Y-%m-%d %H:%M:%S')
		g = f.strftime('%Y-%m-%d %H:%M:%S.%f')

		h = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
		i = h.strftime('%Y-%m-%d %H:%M:%S.%f')

	else:
		pass
	now = datetime.now()
	payments = AgencyPaymentsTable(payment.objects.all().filter(agency = request.user, date_paid__range=[g, i]).order_by('-date_paid'))
	RequestConfig(request, paginate={"per_page": 10}).configure(payments)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, payments)
		return exporter.response('Customer_Payments_Report.{}'.format(export_format))
		
	return render(request, 'dashboard/a-payments.html', {'now':now, 'payments':payments})

def bookings_filter(request):
	if request.method=="POST":
		a = request.POST['start1']
		b = request.POST['end1']
		# f = u''b''
		c = str(datetime(*[int(v) for v in a.replace('T', '-').replace(':', '-').split('-')]))
		d = str(datetime(*[int(v) for v in b.replace('T', '-').replace(':', '-').split('-')]))
		# print(d)
		# s = str(datetime.strptime(c, "%Y-%m-%d %H:%M:%S").date())
		# t = datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date()
		# v = datetime.strptime(c, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S.%f')
		f = datetime.strptime(c, '%Y-%m-%d %H:%M:%S')
		g = f.strftime('%Y-%m-%d %H:%M:%S.%f')

		h = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
		i = h.strftime('%Y-%m-%d %H:%M:%S.%f')
		# dt = datetime.strptime(v, '%Y-%m-%d %H:%M:%S.%f')
		# print(v)
		# e = unicode(v, "utf-8")
		# print(e)
		# print(a)
		# print(b)
	else:
		pass
	now = datetime.now()
	b = ApprovedBookingsTable(booking.objects.all().filter(agency=request.user, approved=True, paid=False, date_added__range=[g, i]).order_by('-date_added'))
	RequestConfig(request, paginate={"per_page": 10}).configure(b)

	export_format = request.GET.get('_export', None)
	if TableExport.is_valid_format(export_format):
		exporter = TableExport(export_format, b)
		return exporter.response('Approved_Bookings_Report.{}'.format(export_format))
	return render(request, 'dashboard/a-booked-approved.html', {'now':now, 'b':b})

def payments1(request):
	now = datetime.now()
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
	return render(request, 'dashboard/a-packages.html', {'a':a})

def unavailable_packages(request):
	b = request.user.get_full_name()
	t = timezone.now()
	s = timezone.now() - timedelta(days=99999)
	a = package.objects.all().filter(Q(agency=request.user), (Q(available=False) | Q(to_day__range=[s,t])))
	return render(request, 'dashboard/a-unavailable-packages.html', {'a':a})

@login_required
def allpackages(request):
	b = request.user.get_full_name()
	t = timezone.now()
	s = timezone.now() + timedelta(days=999999)
	a = package.objects.all().filter(available=True, to_day__range=[t,s])
	e = Hotel.objects.all()
	# instance = get_object_or_404(destination, id=pk)

	if request.method == 'POST':
		form = BookingOptions(request.POST or None)
		if form.is_valid():
			product = form.save(commit=False)
			product.save()

		return redirect('/')
	else:
		form = BookingOptions()

	return render(request, 'dashboard/allpackages.html', {'a':a, 'e':e, 'form':form})

def allpackages1(request):
	b = request.user.get_full_name()
	a = package.objects.all()
	return render(request, 'dashboard/a-allpackages.html', {'a':a})


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
			if a < 1:
				instance.available = False
				# instance.p_slots = a
				# instance.save()
				# print(a)
			else:
				pass
			instance.save()

			messages.info(request, 'Your product was updated successfully')
			return redirect('/ourpackages/')
			
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
	d = package.objects.filter(pk=a.pk).update(available=True)

	# b = a.values_list('p_slots', flat=True)
	# print(b)

	booking.objects.filter(pk=pk).delete()
	return redirect('/dashboard/bookings/')

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
	d = package.objects.filter(pk=a.pk).update(available=True)
	# b = a.values_list('p_slots', flat=True)
	# print(b)

	booking.objects.filter(pk=pk).delete()
	return redirect('/booked/')

def delete_account(request):
	a = request.user.get_username()
	b = User.objects.values_list('id',flat=True).get(username=a)
	User.objects.get(id=b).delete()
	return redirect('/accounts/login/')

class PackageDelete(DeleteView):
    model = package
    success_url = reverse_lazy('ourpackages')

@login_required
# @transaction.atomic
def editprofile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        # profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('/dashboard/profile/edit')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = EditProfileForm(instance=request.user)
        # profile_form = ProfileForm(instance=request.user.profile)
        args = {
        'user_form': user_form,
        # 'profile_form': profile_form
    	}
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
		hotel = request.POST['name7']
		h = Hotel.objects.get(pk=hotel)
		ph = Hotel.objects.values_list('pricep_adult', flat=True).get(pk=hotel)
		price = int(adults)*int(ph)
		p = package.objects.get(pk=pk)

		g = package.objects.values_list('from_day',flat=True).get(pk=pk)
		i = str(g)
		l = package.objects.values_list('to_day',flat=True).get(pk=pk)
		m = str(l)

		date_format = "%Y-%m-%d"
		j = datetime.strptime(start, date_format)
		q = datetime.strptime(end, date_format)
		k = datetime.strptime(i, date_format)
		n = datetime.strptime(m, date_format)

		delta = j - k
		if delta.days < 0:
			messages.info(request,'You can only make a booking from the start date of a package')
			return redirect('/dashboard/pending-bookings/')
		else:
			delta2 = n - j
			if delta2.days < 0:
				messages.info(request,'Your start date cannot be after the end date of a package')
				return redirect('/dashboard/pending-bookings/')
			else:
				delta3 = q - k
				if delta3.days < 0:
					messages.info(request,'Your end date cannot be before the start date of a package')
					return redirect('/dashboard/pending-bookings/')
				else:
					delta4 = n - q
					if delta4.days < 0:
						messages.info(request,'You can only make a booking until the end date of a package')
						return redirect('/dashboard/pending-bookings/')
					else:
						delta5 = q - j
						if delta5.days < 0:
							messages.info(request,'Your start date and end date are in reverse order')
							return redirect('/dashboard/pending-bookings/')
						else:
							a = package.objects.values_list('p_slots',flat=True).get(pk=pk)
							c = int(adults)+int(kids)
							d = int(a)-int(c)
							if d < 0:
								messages.info(request,'The total number of people in your booking exceeds the number of slots available')
								return redirect('/dashboard/pending-bookings/')
							else:
								b = booking.objects.create(user=request.user, user_full=e, clientemail=f, hotel=h, agency=p.agency, agencyname=p.p_agency, agencyemail=p.agencyemail, agencycontact=p.agency_phone, p_name2=p, d_name=p.d_name, adults=adults,kids=kids, pricep_adult=p.pricep_adult, pricep_kid=p.pricep_kid, start_date=start, end_date=end)

								p.p_slots = int(a)-int(c)
								p.save()
								if d < 1:
									# These two lines work too
									# p.available = False
									# p.save()
									e = package.objects.filter(pk=pk).update(available=False)
								else:
									pass
								return redirect('/dashboard/pending-bookings/')
	# except:
		messages.info(request,'There must have been a problem, please try again')
		return redirect('/dashboard/pending-bookings/')
	else:
		form = BookingOptions(request.POST or None)
		return render(request, 'dashboard/pending-bookings.html', {'p':p, 'form':form, 'b':b})

def approve_booking(request, pk):
	a = booking.objects.get(pk=pk).approved
	b = booking.objects.filter(pk=pk).update(approved=True)
	return redirect('/booked/')


@csrf_protect
@ensure_csrf_cookie
def post(request):
	d = request.user
	b = request.user.get_full_name()
	c = request.user.email
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

			package.objects.create(p_name=name,p_category=category,d_name=destination, p_agency=b, agency=d, agencyemail=c, agency_phone=phone,pricep_adult=price1, pricep_kid=price2, from_day=from_date, to_day=to_date,p_slots=slots, available=a, p_description=description)
			return redirect('/ourpackages/')
			messages.info(request, 'Your product was posted successfully')
		else:
			return render(request, 'dashboard/pages/add-package.html',{'form':form})
	else:			
		form = AddPackage()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = AddPackage()
		return render(request, 'dashboard/pages/add-package.html',args)