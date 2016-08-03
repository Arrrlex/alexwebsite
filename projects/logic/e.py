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
	divisor = position + 2
	div_result = divmod(intermediate, divisor)
	return div_result

def next_list_and_e_digit(A):
	"""
	Calculates the next list and the next digit of e.
	:param A: current working list, list
	:return: a tuple, the first component of which is the updated
	list, the second component of which is the next digit of e.
	"""
	B = [x*10 for x in A]
	carry = 0

	# update values of list positions
	for position in range(len(B) - 1, -1, -1):
		carry, new_digit = next_carry_and_digit(B[position], carry, position)
		B[position] = new_digit

	return B, carry

def calculate_e(n):
	"""
	calculates e to n digits.
	:return: e approximation, string
	"""
	A = [1 for i in range(n+1)]

	result_array = []
	while len(result_array) < n-1:
		A, p = next_list_and_e_digit(A)
		result_array.append(p)

	result = [str(x) for x in result_array]
	return '2' + '.' + ''.join(result)
