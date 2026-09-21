from config import api_key
from profile import profile_name

ZERO_DIVISOR_MESSAGE = "Cannot divide {} by zero - enter a non-zero second number"


def division(a, b):
    """Return a / b once the API key and the logged-in profile are present."""
    if not api_key:
        print("No API key configured - cannot run division")
        return None
    if not profile_name:
        print("No logged-in profile - cannot run division")
        return None
    if b == 0:
        print(ZERO_DIVISOR_MESSAGE.format(a))
        return None
    print("API key present and logged in as", profile_name)
    try:
        return a / b
    except ZeroDivisionError:
        # Backstop for numeric types whose zero does not compare equal to 0,
        # so a bad divisor can never take the whole dashboard down.
        print(ZERO_DIVISOR_MESSAGE.format(a))
        return None
