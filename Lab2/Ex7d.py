#Asks the user to input a temperature in fahrenheit
#convert the inputted temperature to celsius and print it out
	
# Name: Edmund Liu
# Date: Sept 4, 2026

def F_to_C(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    rounded_celsius = round(celsius, 2)
    return rounded_celsius

user_temperature = input("enter a temperature in fahrenheit: ")
temperature_float = float(user_temperature)
	
fahrenheit_to_celsius = F_to_C(temperature_float)
	
print("you entered:", user_temperature, "fahrenheit")
print("the temperature that you entered in celsius is:", fahrenheit_to_celsius)
