# Name: Edmund Liu
# Date: Sept 23, 2026

trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fare = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = dict(zip(trip_durations, trip_fare))
print(trips)

trip_num = int(input("what trip do you want?"))

print("The duration of the trip is:", trip_durations[trip_num-1], "miles")
print("The fare of the trip is:", trip_fare[trip_num-1])
