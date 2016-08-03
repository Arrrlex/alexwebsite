from django.shortcuts import render
from django.http import HttpResponse

from os import listdir
from os.path import isdir

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e

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

def pi_submit(request):
	input_string = request.GET['digits']
	try:
		digits = int(input_string)
	except:
		return HttpResponse('Please enter valid number.')
	result = calculate_pi(digits)
	return render(request, 'projects/pi-result.html', {
			'current_page': 'portfolio',
			'digits': digits,
			'result': result,
		})

def e_submit(request):
	input_string = request.GET['digits']
	try:
		digits = int(input_string)
	except:
		return HttpResponse('Please enter valid number.')
	result = calculate_e(digits)
	return render(request, 'projects/e-result.html', {
		'current_page': 'portfolio',
		'digits': digits,
		'result': result,
		})