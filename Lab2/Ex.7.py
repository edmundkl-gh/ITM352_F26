#Asks the user to input a temperature in fahrenheit
#convert the inputted temperature to celsius and print it out

# Name: Edmund Liu
# Date: Sept 4, 2026

user_temperature = float(input("enter a temperature in fahrenheit: "))
fahrenheit_to_celsius= (user_temperature - 32) *5/9
print("the temperature that you entered in celsius is:", fahrenheit_to_celsius)