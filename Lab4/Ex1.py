#Ask the user to enter first name, middle initial, and last name
#Prints the full name

first = input("Enter your first name: ")
middle = input("Enter your middle initial: ")
last = input("Enter your last name: ")

full_name = first + " " + middle + ". " + last
print("Your full name is:", full_name)

print(f"Your full name is: {first} {middle}. {last}")
print("Your full name using " + "%" + " formatting is: %s %s. %s" %(first, middle, last))
print("Your full name using format method is: {} {}. {}".format(first, middle, last))
print("Your full name using list joins is:" + " ".join([first, middle + ".", last]))
