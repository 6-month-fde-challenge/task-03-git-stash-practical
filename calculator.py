"""Entry point that ties the arithmetic modules together."""

from input_variables import a, b
from addition_module import addition
from subtract_module import subtract
from multiply_module import multiply
from division_module import division

total = addition(a, b)
subtraction = subtract(a, b)
multiplication = multiply(a, b)
div = division(a, b)

if __name__ == "__main__":
    print("Addition of the two numbers is       : ", total)
    print("Subtraction of the two numbers is    : ", subtraction)
    print("Multiplication of the two numbers is : ", multiplication)
    print("Division of the two numbers is       : ", div)
