import math


def decimal_to_binary(d):
    """

    :param d: int, decimal representation of number
    :return: string, binary representation of number
    """
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
