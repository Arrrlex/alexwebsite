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
from projects.logic.tiling import get_tiles, birds_eye, cut_tiles

def write_prime_factors(x):
    """
    Takes an integer x, and returns html describing the decomposition of x 
    into prime factors.
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



def basic_projects(request, current_page):

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

	context = {'current_page': current_page, 'func':'calculate_pi', 
		'arg': '50'}
	render_karan = lambda context: render(request, 
		'projects/applet-karan.html', context)
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
		context['error_message'] = (
			'For this script, please choose a number between 1 and {}'.format(
				func_max[1]))
		return render_karan(context)
	try:
		result = func_max[0](arg)
	except AssertionError:
		context['error_message'] = 'Please choose a valid number'
		return render_karan(context)
	context.update({'arg': arg, 'result': result})
	return render_karan(context)

def tiling(request, current_page):
	try:
		width, height, side_length, cost_per_tile = (
			request.GET['width'], 
			request.GET['height'],
			request.GET['side_length'], 
			request.GET['cost_per_tile'])
	except:
		return render(
			request, 'projects/tiling-applet.html')

	width, height, side_length, cost_per_tile = (
		float(width), float(height), float(side_length), float(cost_per_tile))
	total_tiles, extra_tiles = get_tiles(width, height, side_length)
	return render(
		request,
		'projects/tiling-applet.html', 
		{
			'width': width,
			'height': height,
			'side_length': side_length,
			'cost_per_tile': cost_per_tile,
			'current_page': current_page,
			'scale_factor': 100 * height / width,
			'result': True,
			'total_cost': total_tiles * cost_per_tile,
			'total_tiles': total_tiles,
			'birds_eye': birds_eye(
				side_length, width, height),
			'cut_tiles': cut_tiles(side_length, extra_tiles),
			'norm_width': 700,
			'norm_height': height * 700 / width,
			'current_page': current_page
		})