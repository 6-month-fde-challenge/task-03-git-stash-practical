"""Derive the profile name from the login details.

profile_name is initialised to an empty string first. Previously it was only
assigned inside the `if` block, so blank input left the name undefined and every
module importing it failed.
"""

from login import user_name, pass_word

profile_name = ""

if user_name and pass_word:
    profile_name = user_name
