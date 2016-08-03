import math

def binary_to_decimal(s):
    """

    :param s: string, binary representation of number
    :return: string, decimal representation of number
    """
    result = 0
    
    for i in range(0, len(s)):
        result += int(s[i]) * 2 ** (len(s) - 1 - i)
        
    return str(result)

def decimal_to_binary(d):
    """

    :param d: string, decimal representation of number
    :return: string, binary representation of number
    """
    d = int(d)
    result = ""
    place = 0
    while 2 ** (place + 1) < d:
        place += 1

    while place >= 0:
        x = 2 ** place
        if x <= d:
            result += "1"
            d -= x
        else:
            result += "0"
        place -= 1

    return result
