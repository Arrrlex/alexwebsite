from django.shortcuts import render
from django.http import HttpResponse

from os import listdir
from os.path import isdir

projlist = [dir for dir in listdir() if isdir(dir)]

def index(request):
	return render(request, 'projects/index.html', {'current_page': 'portfolio'})

def pi(request):
	return render(request, 'projects/pi.html', {'current_page': 'portfolio'})

def e(request):
	return render(request, 'projects/e.html', {'current_page': 'portfolio'})

def fibonacci(request):
	return HttpResponse('Dummy View.')

def prime_factors(request):
	return HttpResponse('Dummy View.')

def binary_converter(request):
	return HttpResponse('Dummy View.')