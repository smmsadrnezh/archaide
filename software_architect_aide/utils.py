import string
import random


def get_random_string():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(7))
    return result_str
