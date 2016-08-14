from timeit import timeit
import random

def time_function(func, import_location, arg):
	print('Arg: {}'.format(arg))
	stmt = '{}({})'.format(func, arg)
	stup = 'from {} import {}'.format(import_location, func)
	timetaken = timeit(stmt, stup, number=1)
	print('Time: {}'.format(timetaken))
	return timetaken

def find_timeout_level(func, import_location='__main__', timeout=2):
	timetaken = 0
	arg = 1
	while timetaken < timeout:
		arg = random.randint(arg*2, arg*3)
		timetaken = time_function(func, import_location, arg)
	upper_bound = arg
	lower_bound = arg // 2
	for i in range(10):
		new = (upper_bound + lower_bound)//2
		if new == upper_bound or new == lower_bound:
			break
		timetaken = time_function(func, import_location, new)
		if timetaken < timeout:
			lower_bound = new
		else:
			upper_bound = new

	return lower_bound