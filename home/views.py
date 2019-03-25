from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import EmailMessage
from dashboard.models import destination, package, booking, Hotel, payment

# Create your views here.
def home(request):
    d = destination.objects.all()
    return render(request, 'home/homepage.html', {'d':d})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            bodyy =''.join(['From: ', from_email, '    Feedback: ', message])
            try:
                send_mail(name, bodyy, from_email, ['vicngetichvictor@gmail.com', 'thekenyanthrill@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')



            return redirect('emailsuccess')
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})