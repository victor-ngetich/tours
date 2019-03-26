from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from dashboard.models import destination, package, booking, Hotel, payment
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages

# Create your views here.

def payprocess(request, pk=None):
    # order_id = request.session.get('order_id')
    product = get_object_or_404(booking, pk=pk)
    print (product)
    # host = request.get_host()
    # a = booking.objects.get(pk=pk)
    # print(a)
    # What you want the button to do.
    paypal_dict = {
        "business": "vicngetichvictor@gmail.com",
        "amount": "130.00",
		"currency_code": "USD",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('paydone')),
        "cancel_return": request.build_absolute_uri(reverse('paycancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, 'product':product}
    return render(request, "payment/process.html", context)

@csrf_exempt
def paydone(request):
    a = request.GET.get('amt', None)
    # b = request.GET.get('cm', None)
    c = request.GET.get('item_name', None)
    d = request.GET.get('item_number', None)
    e = request.GET.get('st', None)
    f = request.GET.get('tx', None)
    g = request.GET.get('user', None)
    h = request.GET.get('packageid', None)
    user = request.user.get_username()

    # try:
    if payment.objects.filter(transaction_id=f).exists():
        return HttpResponseRedirect('/dashboard/bookings/')
    else:
        i = booking.objects.get(id=d)
        j = payment.objects.create(booking=i, user=request.user, user_full=i.user_full, agencyemail=i.agencyemail, clientemail=i.clientemail, hotel=i.hotel, agency=i.agency, agencyname=i.agencyname, agencycontact=i.agencycontact, date_added=i.date_added, adults=i.adults,kids=i.kids, pricep_adult=i.pricep_adult, pricep_kid=i.pricep_kid, amountpaid=a, start_date=i.start_date, end_date=i.end_date, days=i.days, transaction_status=e,transaction_id=f)
        k = booking.objects.get(pk=d).paid
        l = booking.objects.filter(pk=d).update(paid=True)
    # except:
    # messages.info(request,'There must have been a problem, please try again')
    return render (request, "payment/done.html")

@csrf_exempt
def paycancel(request):
    return render (request, "payment/cancelled.html")