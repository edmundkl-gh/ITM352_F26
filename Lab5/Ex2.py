# Define a list of dictionaries where each dictionary represents a trip
# Name: Edmund Liu
# Date: Sept 23, 2026

trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fare = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = {
    "miles":trip_durations,
    "fares":trip_fare
}

print(trips)

print("The duration of the 3rd trip is:", trips["miles"][2], "miles")
print("The fare of the 3rd trip is:", trips["fares"][2])

