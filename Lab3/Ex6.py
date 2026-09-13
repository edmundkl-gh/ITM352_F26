# rewrite the code to use the functions from the HandyMath module instead of defining them in this file 
# Name: Edmund Liu
# Date: Sept. 11, 2026
from HandyMath import max, min, midpoint, squareroot, exponent

num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

print(f"The midpoint of {num1} and {num2} is {midpoint(num1, num2)}")
print(f"The square root of the square of {num1} is {squareroot(num1 ** 2)}")
print(f"{num1} raised to the power of {num2} is {exponent(num1, num2)}")
print(f"The max of {num1} and {num2} is {max(num1, num2)}")
print(f"The min of {num1} and {num2} is {min(num1, num2)}")