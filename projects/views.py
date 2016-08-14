from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from os import listdir
from os.path import isdir

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib
from projects.logic.prime_factors import prime_factors
from projects.logic.binary_converter import decimal_to_binary
from projects.logic.next_prime import first_k_primes

def write_prime_factors(x):
    """
    Takes an integer x, and returns html describing the decomposition of x into prime factors.
    For example: the input "40" gives the string
    "2<sup>3</sup> &times; 5"
    which evaluates to the equivalent of the expression
    "2**3 * 5"
    """
    factors = prime_factors(x)
    result_list = []
    for factor, exponent in factors.items():
        if exponent == 1:
            result_list.append(str(factor))
        else:
            to_append = '{0}<sup>{1}</sup>'.format(factor, exponent)
            result_list.append(to_append)
    return ' &times; '.join(result_list)

# The first item in each tuple is the function to be called.
# The second item is the maximum argument size, corresponding to the server
# taking roughly 2 seconds to compute the function with that input. This
# was calculated using find_timeout_level in logic/timing_functions.py

func_dict = {
	'pi': (calculate_pi, 878), 
	'e': (calculate_e, 1937), 
	'fib': ((lambda x: str(fib(x))), 1554857), 
	'prime_factors': (write_prime_factors, 1000000), 
	'to_binary': (decimal_to_binary, 10000000),
	'primes_list': (first_k_primes, 1000)
}

def karan_project(request, current_page):
	context = {'current_page': current_page, 'func':'calculate_pi', 'arg': '50'}
	render_karan = lambda context: render(request, 'projects/applet-karan.html', context)
	try:
		input_arg = request.GET['arg']
		context['arg'] = input_arg
	except:
		return render_karan(context)
	try:
		input_func = request.GET['func']
		context['func'] = input_func
	except:
		return render_karan(context)
	try:
		arg = int(input_arg)
	except ValueError:
		context['error_message'] = 'Please enter a valid number'
		return render_karan(context)
	try:
		func_max = func_dict[input_func]
	except:
		context['error_message'] = 'Please choose a valid script'
		return render_karan(context)
	if not 1 <= arg <= func_max[1]:
		context['error_message'] = 'For this script, please choose a number between 1 and {}'.format(func_max[1])
		return render_karan(context)
	try:
		result = func_max[0](arg)
	except AssertionError:
		context['error_message'] = 'Please choose a valid number'
		return render_karan(context)
	context.update({'arg': arg, 'result': result})
	return render_karan(context)