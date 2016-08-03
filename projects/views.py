from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from os import listdir
from os.path import isdir

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib

def prime_factors(request):
	return HttpResponse('Dummy View.')

def binary_converter(request):
	return HttpResponse('Dummy View.')

def project(request, current_page, template_page, submit, calculate):
	context = {'current_page': current_page, 'submit': submit}
	try:
		input_string = request.GET['arg']
	except:
		return render(request, template_page, context)
	try:
		arg = int(input_string)
	except:
		context['error_message'] = 'Please enter a valid number'
		return render(request, template_page, context)
	if not 1 <= arg <= 1000:
		context['error_message'] = 'Please enter a number between 1 and 1000, to avoid large strain on the server.'
		return render(request, template_page, context)
	result = calculate(arg)
	context.update({'arg': arg, 'result': result})
	return render(request, template_page, context)