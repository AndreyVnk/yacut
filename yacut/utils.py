from random import shuffle
from string import ascii_letters, digits

ALLOWED_SYMBOLS = ascii_letters + digits
MAX_LENGTH = 16


def get_unique_short_id():
    symbols = list(ALLOWED_SYMBOLS)
    shuffle(symbols)
    return ''.join(symbols[:6])


def check_allowed_symbols(custom_id):
    for symbol in custom_id:
        if symbol not in ALLOWED_SYMBOLS:
            return False
    return True
