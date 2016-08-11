fib_dict = {1:1, 2:1}

def fib(n):
    if n not in fib_dict:
        fib_dict[n] = fib(n-1) + fib(n-2)

    return fib_dict[n]

def fib_str(n):
	return str(fib(n))