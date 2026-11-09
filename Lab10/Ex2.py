# Create a pandas dataframe from individual lists
# Do some simple stats on the data
import pandas as pd

# List of individuals' names, ages, and genders
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

raw_data = zip(ages, gender)

# Create a pandas dataframe from the lists
df = pd.DataFrame(raw_data, columns=["Age", "Gender"], index=names)

summary = df.describe()
print(summary) # Prints summary of statistics

# Calculate the average age by gender
average_age_by_gender = df.groupby("Gender")["Age"].mean()
print("\nAverage Age by Gender:")
print(average_age_by_gender)
 