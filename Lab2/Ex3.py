# Ask the user to enter a decimal number. Calculate the square root of that number and print it out.
# Name: Edmund Liu
# Date: Sept 2, 2026

#Use input() to get a floating point number from the user. Use float() to convert the input to a float
#Use the ** operator to calculate the square of the number. Use print() to print out the result.
input_value = input("Enter a floating point number: ")
float_value = float(input_value)
squared_value = float_value ** 2

#print out the original number and the squared value. Use round() to round the squared value to two decimal places.
print("you entered:", float_value)
print("The square of the number you entered is:", squared_value)
