from config import api_key
from profile import profile_name


def multiply(a, b):
    """Return a * b once the API key and the logged-in profile are present."""
    if not api_key:
        print("No API key configured - cannot run multiplication")
        return None
    if not profile_name:
        print("No logged-in profile - cannot run multiplication")
        return None
    print("API key present and logged in as", profile_name)
    return a * b
