"""Very small login step for the project.

Like input_variables.py, the prompts fall back to defaults so the program stays
runnable when there is no interactive terminal.
"""


def read_text(prompt, default):
    try:
        value = input(prompt)
    except EOFError:
        value = ""
    if not value:
        print("   -> no input available, using default:", default)
        return default
    return value


user_name = read_text("Enter username : ", "veerandra")
pass_word = read_text("Enter password : ", "demo-password")
