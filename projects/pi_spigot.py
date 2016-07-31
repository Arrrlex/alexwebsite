import math

def next_carry_and_digit(digit, carry, position):
	"""
	Perform intermediate calculation for regularising the list.
	:param digit: the digit currently in position "position" of 
	working list, int
	:param carry: outputted from next_regular in position + 1 to
	be added to digit, int
	:param position: the position in the working list we are 
	generating the next digit of
	:return: a tuple, the first component of which is the carry
	from this position, the second component is the updated digit
	"""
	intermediate = digit + carry
	divisor = 2 * position + 1
	div_result = divmod(intermediate, divisor)
	return (position * div_result[0], div_result[1])

def next_list_and_predigit(A):
	"""
	Calculates the next list and the next predigit.
	:param A: current working list, list
	:return: a tuple, the first component of which is the updated
	list, the second component of which is the next predigit
	"""
	B = [x*10 for x in A]
	carry = 0

	# update values for list positions other than 0
	for position in range(len(A)-1, 0, -1):
		carry, new_digit = next_carry_and_digit(B[position], carry, position)
		B[position] = new_digit

	# update value for list position 0 and calculate predigit
	predigit, B[0] = divmod(B[0] + carry, 10)

	return (B, predigit)

def adjust_predigits(predigits, p):
	"""
	Given the current held predigits (a list of integers) and the latest
	candidate, returns a tuple:
	(predigits to be held, digits to be added onto current pi result)
	"""
	if p == 9:
		return (predigits + [p], [])
	elif p == 10:
		#increment (mod 10) all values in predigits
		new_values = [(x+1) % 10 for x in predigits]
		#release these as digits of pi. Hold 0 as predigit
		return ([0], new_values)
	else:
		#release all values in predigits, hold p as predigit
		return ([p], predigits)

def calculate_pi(n):
	"""
	Calculates pi to n digits.
	:return: pi approximation, string
	"""

	# Initialise A as a list of 2s, long enough not to cause problems
	A = [2 for i in range(math.floor(10*n / 3) + 1)]

	result_array, predigits = [], []
	while len(result_array) < n:
		A, p = next_list_and_predigit(A)
		predigits, add_to_result_array = adjust_predigits(predigits, p)
		result_array += add_to_result_array

	result = [str(x) for x in result_array]
	return result[0] + '.' + ''.join(result[1:])


