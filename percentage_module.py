"""Express the first number as a percentage of the second."""

from config import api_key
from profile import profile_name

ZERO_BASE_MESSAGE = "Cannot express {} as a percentage of zero"


def percentage(a, b):
    """Return a as a percentage of b, or None when the operation is not safe."""
    if not api_key:
        print("No API key configured - cannot run percentage")
        return None
    if not profile_name:
        print("No logged-in profile - cannot run percentage")
        return None
    if b == 0:
        print(ZERO_BASE_MESSAGE.format(a))
        return None
    print("API key present and logged in as", profile_name)
    try:
        return (a / b) * 100
    except ZeroDivisionError:
        print(ZERO_BASE_MESSAGE.format(a))
        return None
