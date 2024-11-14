"Helper functions and constants for github REST APIs testing"

import string
import random


USER_NAME = "test-user-1511"
ACCOUNT_ID = 188383201

INVALID_NAME = "--**--"
MAX_ID = int("0x7FFFFFFF", 16)

MAX_PAGINATION = 100


def random_string(size: int = 20):
    chars = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choice(chars) for _ in range(size))
