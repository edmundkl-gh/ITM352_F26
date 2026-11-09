import csv
import os

if not os.path.exists("window_cleaning_employees.csv"):
    print("Error: File window_cleaning_employees.csv not found.")
    exit(1)

if not os.access("window_cleaning_employees.csv", os.R_OK):
    print("Error: File window_cleaning_employees.csv is not readable.")
    exit(1)
else:
     file_size = os.path.getsize("window_cleaning_employees.csv")
     print(f"File exists and is readable. Size: {file_size} bytes")


csv_filename = "window_cleaning_employees.csv"
salaries = []

# Read the csv file and store the salaries in a list
with open(csv_filename, "r") as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader)
    print(f"Headers: {headers}")
    salary_index = headers.index("Annual_Salary")
    for row in reader:
            salary = float(row[salary_index])
            salaries.append(salary)

    avg_salary = sum(salaries) / len(salaries)
    min_salary = min(salaries)
    max_salary = max(salaries)

    print(f"Average Salary: ${avg_salary:.2f}")
    print(f"Minimum Salary: ${min_salary:.2f}")
    print(f"Maximum Salary: ${max_salary:.2f}")