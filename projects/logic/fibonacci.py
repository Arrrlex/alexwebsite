# We use the following two identities:
# fib(2*k) = fib(k)*(2*fib(k+1)-fib(k))
# fib(2*k + 1) = fib(k+1)**2 + fib(k)**2

def fib(n):
	op_stack = []
	curr, next = 1, 1
	while n != 1:
		if n % 2 == 0:
			n = n / 2
			op_stack.append("double")
		else:
			n -= 1
			op_stack.append("increment")
	while len(op_stack) != 0:
		op = op_stack.pop()
		if op == "double":
			n *= 2
			curr, next = (
				curr * (2 * next - curr),
				curr**2 + next**2)
		if op == "increment":
			n += 1
			curr, next = (
				next,
				curr + next)
	return curr
