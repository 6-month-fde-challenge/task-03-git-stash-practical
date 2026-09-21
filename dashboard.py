"""Final integration point - displays the results produced by calculator.py."""

from calculator import total, subtraction, multiplication, div
from input_variables import a, b
from percentage_module import percentage

pct = percentage(a, b)

print("*************** DASHBOARD ***************")
print("Result of addition is       : ", total)
print("Result of subtraction is    : ", subtraction)
print("Result of multiplication is : ", multiplication)
print("Result of division is       : ", div)
print("Result of percentage is     : ", pct)
print("*****************************************")
