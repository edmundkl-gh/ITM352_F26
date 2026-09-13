import HandyMath

num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

print(f"The midpoint of {num1} and {num2} is {HandyMath.midpoint(num1, num2)}")
print(f"The square root of the square of {num1} is {HandyMath.squareroot(num1 ** 2)}")
print(f"{num1} raised to the power of {num2} is {HandyMath.exponent(num1, num2)}")
print(f"The max of {num1} and {num2} is {HandyMath.max(num1, num2)}")
print(f"The min of {num1} and {num2} is {HandyMath.min(num1, num2)}")
