from timeit import timeit
import random

def time_function(func, import_location, arg, repeat=3):
	print('Arg: {}'.format(arg))
	stmt = '{}({})'.format(func, arg)
	stup = 'from {} import {}'.format(import_location, func)
	timetaken = timeit(stmt, stup, number=repeat)/repeat
	print('Time: {}'.format(timetaken))
	return timetaken

def find_timeout_level(func, import_location='__main__', timeout=2, trials=5):
	results = []
	for i in range(trials):
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
		results.append(lower_bound)
		print('------')
	result = sum(results)/len(results)
	return result

# Running find_timeout_level on server for various functions and timeout=2:

# calculate_pi: 878.4
# calculate_e: 1937
# fib: 7 198 655.4
# fib_str: 1 554 857.2
# write_prime_factors: 8 460 216 943 (data not consistent though)
# decimal_to_binary: as large as you like
# primes_list: not applicable (hard argument limit set by sieve size)