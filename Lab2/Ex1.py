# This program prompts the user to enter a number between 1 and 100, calculates the square of that
# number,
# Name: Edmund Liu
# Date: Sept. 2, 2026
value_entered = input("Enter a number between 1 and 100:")
value_as_integer = int(value_entered)

value_squared = value_as_integer ** 2

print("you entered:", value_as_integer)
print("the square of your number is:", value_squared)

print(f"you entered: {value_as_integer}, and the square of {value_as_integer} is: {value_squared}")

