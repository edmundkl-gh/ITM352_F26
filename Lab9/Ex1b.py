# Open a file using with

with open("names.txt", "r") as file_object:
    print(file_object.read())

print("File closed:", file_object.closed)
