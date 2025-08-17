from random import choice
from string import ascii_lowercase, digits


def get_random_string(length):
    chars = ascii_lowercase + digits
    return str(''.join(choice(chars) for _ in range(length)))


# print(get_random_string(04))



def get_random_digit(length):
    chars = digits
    return str(''.join(choice(chars) for _ in range(length)))

