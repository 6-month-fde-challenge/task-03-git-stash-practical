from config import api_key
from profile import profile_name


def division(a, b):
    """Return a / b once the API key and the logged-in profile are present."""
    if not api_key:
        print("No API key configured - cannot run division")
        return None
    if not profile_name:
        print("No logged-in profile - cannot run division")
        return None
    if b == 0:
        print("Cannot divide by zero")
        return None
    print("API key present and logged in as", profile_name)
    return a / b
