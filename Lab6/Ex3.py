# Determine movie pice. The rules are:
# - The normal price is $14
# - If someone is 65 or older, they pay $8.
# - If it is Tuesday, the price is $10.
# - If it is a matinee, the price is $5 for seniors and $8 otherwise
# Name: Edmund Liu
# Date: Sept. 25, 2026

price = 14

day = input("Enter the Day of the week").strip().lower()
age = int(input("Enter your age"))
matinee = input("Is it a matinee? (yes/no)") == "yes"

if day == "tuesday":
    price = 10
if age >= 65:
    price = 8
if matinee:
    if age >= 65:
        price = 5
    else:
        price = 8

print("The ticket price is: $" + str(price))
