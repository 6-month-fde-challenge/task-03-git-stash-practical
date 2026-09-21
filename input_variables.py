"""Collect the two numbers the calculator works with.

input() is wrapped so the project also runs non-interactively (for example when
a reviewer pipes no stdin), instead of crashing with EOFError.
"""


def read_number(prompt, default):
    try:
        return int(input(prompt))
    except (EOFError, ValueError):
        print("   -> no input available, using default:", default)
        return default


a = read_number("Enter a number 1 : ", 10)
b = read_number("Enter a number 2 : ", 5)
