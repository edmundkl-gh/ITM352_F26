# Define a list of servey response value (5, 7, 3, 8) and store them
# in a variable, Define a tuple of response IDs (1012, 1035, 1021, and 1053).
# add these to the list

response_values = [5, 7, 3, 8]
response_values.sort()
response_ids = (1012, 1035, 1021, 1053)
response_values.append(response_ids)

print("combined response values and IDs:", response_values)

response_values_new = [(1012, 5), (1035, 7), (1021, 3), (1053, 8)]