from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from os import listdir
from os.path import isdir

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib_str
from projects.logic.prime_factors import write_prime_factors
from projects.logic.binary_converter import decimal_to_binary

func_dict = {
	'pi': 'calculate_pi', 
	'e': 'calculate_e', 
	'fib': 'fib_str', 
	'prime_factors': 'write_prime_factors', 
	'to_binary': 'decimal_to_binary',
}

def karan_project(request, current_page):
	context = {'current_page': current_page, 'func':'calculate_pi', 'arg': '50'}
	try:
		input_arg = request.GET['arg']
		context['arg'] = input_arg
	except:
		return render(request, 'projects/applet-karan.html', context)
	try:
		input_func = request.GET['func']
		context['func'] = input_func
	except:
		return render(request, 'projects/applet-karan.html', context)
	try:
		arg = int(input_arg)
	except ValueError:
		context['error_message'] = 'Please enter a valid number'
		return render(request, 'projects/applet-karan.html', context)
	if not 1 <= arg <= 1000:
		context['error_message'] = 'Please enter a number between 1 and 1000, to avoid large strain on the server.'
		return render(request, 'projects/applet-karan.html', context)
	try:
		fun = eval(func_dict[input_func])
	except:
		context['error_message'] = 'Please choose a valid script'
		return render(request, 'projects/applet-karan.html', context)
	try:
		result = fun(arg)
	except AssertionError:
		context['error_message'] = 'Please choose a valid number'
	context.update({'arg': arg, 'result': result})
	return render(request, 'projects/applet-karan.html', context)