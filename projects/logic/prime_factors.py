from collections import Counter

def prime_factors(x):
    l = []
    n = 2
    while x != 1:
        if x % n == 0:
            l.append(n)
            x = x / n
        else:
            n += 1

    factors = dict(Counter(l))
    print "Prime factors: {}".format(factors)
    #hi
