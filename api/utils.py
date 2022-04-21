import random


def create_new_iban_number():
    return str(random.randint(1000000000, 9999999999))
