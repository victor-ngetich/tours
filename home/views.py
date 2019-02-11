from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/homepage.html')

def contact(request):
    return render(request, 'home/contact.html')

def explore(request):
    return render(request, 'home/explore.html')