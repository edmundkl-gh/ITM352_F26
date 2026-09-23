# Define trip durations and fares as a list of dictionaries
# Name: Edmund Liu
# Date: Sept 23, 2026

trips = [
{"duration":1.1, "Fare":"$6.25"},
{"duration":0.8, "Fare":"$5.25"},
{"duration":2.5, "Fare":"$10.50"},
{"duration":2.6, "Fare":"$8.05"}
]

print(trips)
print("The duration of the 3rd trip is:", trips[2]["Trip_duration"], "miles")
print(f"The fare of the 3rd trip is {trips[2]['Fare']:.2f}")
