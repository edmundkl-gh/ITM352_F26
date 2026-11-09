#Open a file of names and print its type

file_object = open("names.txt", "r")
print(file_object.read())
file_object.close()
