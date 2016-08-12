# Sieve of Erastothenes

def first_k_primes(k):
	"""
	Outputs a string of the first k primes separated by commas
	"""
	sieve = [i for i in range(1, 8000)]
	divisor = 2
	primes = [2]
	primes_counter = 1
	while primes_counter < k:
		# remove from sieve all those divisible by divisor
		for i in sieve[sieve.index(divisor)+1:]:
			if i % divisor == 0:
				sieve.remove(i)

		divisor = sieve[sieve.index(divisor) + 1]
		primes.append(divisor)
		primes_counter += 1

	return ', '.join(map(str, primes))
