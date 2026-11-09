import csv
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