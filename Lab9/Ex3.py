# Read taxi_1000,csv and calculate the total of all fares, average far,
# and the max trip distance.

import csv
filename = "..\\taxi_1000.csv"

with open(filename, "r") as file:
    csv_reader = csv.reader(file)

    Total_fare = 0.0
    Max_distance = 0.0
    average_fare = 0.0
    num_rows = 0

    for row in csv_reader:
        if num_rows == 0:
            # Skip the header row
            fare_index = row.index("Fare")
            distanec_index = row.index("Trip Miles")
            num_rows += 1
            continue

        if (num_rows > 0):
            fare = float(row[fare_index])
            distance = float(row[distanec_index])

            Total_fare += fare
            if distance > Max_distance:
                Max_distance = distance

        num_rows += 1

if num_rows > 1:
    average_fare = Total_fare / (num_rows - 1)  # Subtract 1 for the header row

print(f"Total Fare: ${Total_fare:.2f}")
print(f"Average Fare: ${average_fare:.2f}")
print(f"Maximum Trip Distance: {Max_distance:.2f} miles")