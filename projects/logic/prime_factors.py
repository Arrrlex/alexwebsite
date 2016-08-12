from collections import Counter

def prime_factors(x):
    """
    Takes an integer argument x, and returns a dictionary giving the prime factors of x and
    the exponent of each prime factor in x.
    """

    l = []
    n = 2
    while x != 1:
        if x % n == 0:
            l.append(n)
            x = x / n
        else:
            n += 1

    factors = dict(Counter(l))
    return factors