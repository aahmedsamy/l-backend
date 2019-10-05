from random import randint


def gen_rand_number_with_length(length):
    """
    generates random number with desired length
    """
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return randint(range_start, range_end)


def gen_rand_number_between(start, end):
    """
    generates random number between two integers
    """
    return randint(start, end)


def check_if_numbers(num):
    for i in num:
        if "0" <= i <= "9":
            return True
    return False
