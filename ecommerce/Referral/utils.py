import random


def _generate_code():
    t = "abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
    return "".join([random.choice(t) for i in range(40)])