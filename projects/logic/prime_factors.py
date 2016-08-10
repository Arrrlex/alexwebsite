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