# Manipulate a list in various tricky ways
# Name: Edmund Liu
# Date: Sept. 16, 2026

response_values = [5, 7, 3, 8]
response_values.append(0)
print("response values after appending is:", response_values)
response_values.insert(2, 6)
response_values = response_values[:2] + [6] + response_values[2:]
print("response values after inserting 6 at index 2 is:", response_values)
