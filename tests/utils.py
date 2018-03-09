import random
import string


def gen_string(l):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(l)
    )
