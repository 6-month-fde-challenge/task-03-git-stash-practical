"""Configuration for the calculator project.

The API key is read from the API_KEY environment variable. A harmless demo
value is used as a fallback so that a fresh clone of this repository runs
without any setup.

This module replaces the old `secrets.py`. The previous version was listed in
.gitignore, so it never reached GitHub and `from secrets import api_key`
silently resolved to Python's standard-library `secrets` module, which does not
define `api_key`. That made the program crash on a fresh clone.
"""

import os

api_key = os.getenv("API_KEY", "demo-api-key-not-a-real-secret")
