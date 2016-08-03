from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'pages/index.html', {'current_page': 'index'})

def cv_index(request):
	return render(request, 'pages/cv.html', {'current_page': 'cv'})

def contact(request):
	return render(request, 'pages/contact.html', {'current_page': 'contact'})
