import random
import string


def make_random_str():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(25))


def make_random_int():
    return random.randint(1, 999_999_999)


def create_random_args(*args):
    random_args = {}
    for arg in args:
        random_args[arg] = make_random_str()
    return random_args
