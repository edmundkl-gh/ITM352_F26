

# Loading the data: load_sales_data() reads the CSV file from Google Drive,
# times how long it takes, and saves a copy on your computer.
# If something goes wrong, it returns an error message instead of crashing.
# main() shows that message and stops the program.
# Missing data: clean_data() changes every empty value to 0.
# Missing columns: main() warns you at the start. Each analysis also checks
# that it has the columns it needs.
# Menu: MENU_ITEMS is a list of (label, function) pairs. To add, remove or
# move a menu item, change only that list. The numbers update by themselves.
# Every analysis RETURNS its pivot table. It does not print it. The menu
# loop prints the table. Because the tables are returned, we can also show
# two of them side by side (individual task 1).
# Safe code: try/except handles file problems. Loops keep asking until the
# user types a valid answer. assert checks for mistakes made by the
# programmer (for example, passing the wrong type of data).
# Easy to change: all column names are constants near the top. If your CSV
# uses different names, change them there and nowhere else.

# Name: Edmund Liu
# Date: Nov. 8, 2026


import sys
import time

import pandas as pd

DATA_FILE_ID = "1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
DATA_URL = "https://drive.google.com/uc?export=download&id=" + DATA_FILE_ID
LOCAL_FILE_NAME = "sales_data.csv"

COL_REGION = "sales_region"
COL_STATE = "state"
COL_ORDER_TYPE = "order_type"
COL_CUSTOMER_TYPE = "customer_type"
COL_PRODUCT = "product_name"
COL_CATEGORY = "product_category"
COL_QUANTITY = "quantity"
COL_PRICE = "sale_price"
COL_EMPLOYEE = "employee_name"

REQUIRED_COLUMNS = [
    COL_REGION, COL_STATE, COL_ORDER_TYPE, COL_CUSTOMER_TYPE, COL_PRODUCT,
    COL_CATEGORY, COL_QUANTITY, COL_PRICE, COL_EMPLOYEE,
]
NUMERIC_COLUMNS = [COL_QUANTITY, COL_PRICE]

PIVOT_ROW_CHOICES = [COL_EMPLOYEE, COL_REGION, COL_CATEGORY]
PIVOT_COLUMN_CHOICES = [COL_ORDER_TYPE, COL_CUSTOMER_TYPE]
PIVOT_VALUE_CHOICES = [COL_QUANTITY, COL_PRICE]
PIVOT_AGGREGATIONS = ["sum", "mean", "count"]

def clean_data(data):
    """Return a cleaned copy of the data. Empty values become 0."""
    assert isinstance(data, pd.DataFrame), "clean_data needs a DataFrame"

    cleaned = data.copy()

    # Remove extra spaces around the column names.
    new_names = []
    for name in cleaned.columns:
        new_names.append(str(name).strip())
    cleaned.columns = new_names

    # Turn the number columns into real numbers. Bad text such as "abc"
    # becomes empty, and then becomes 0 on the last line.
    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    return cleaned.fillna(0)


def load_sales_data(source, local_copy_name):

    # Read the CSV file from source (a web address or a file name).
    # Returns three things: (data, seconds, error_message).
    # If it worked, error_message is "". If not, data is None.
    start_time = time.time()

    try:
        data = pd.read_csv(source)
    except (OSError, ValueError) as error:
        return None, 0, "Could not read the data file: " + str(error)

    if len(data) == 0:
        return None, 0, "The data file has no rows of data."

    # If the Drive file is not shared, Google sends a web page instead of
    # the CSV. pandas reads that page as a table with only one column,
    # so a one-column table means something went wrong.
    if len(data.columns) < 2:
        return None, 0, ("The file does not look like a sales CSV. If it is "
                         "on Google Drive, share it as 'Anyone with the link'.")

    # Save a copy on this computer. If saving fails, just warn the user.
    try:
        data.to_csv(local_copy_name, index=False)
    except OSError as error:
        print("Warning: could not save a local copy: " + str(error))

    data = clean_data(data)
    seconds = time.time() - start_time
    return data, seconds, ""


def missing_columns(data, needed_columns):
    """Return the names from needed_columns that are not in the data."""
    missing = []
    for name in needed_columns:
        if name not in data.columns:
            missing.append(name)
    return missing


def require_columns(data, needed_columns):
    """Return True if all columns exist. If not, print why and return False."""
    missing = missing_columns(data, needed_columns)
    if len(missing) > 0:
        print("This analysis cannot run. Missing column(s): "
              + ", ".join(missing))
        return False
    return True


def read_int_in_range(prompt, low, high):
    """Keep asking until the user types a whole number from low to high."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print("Invalid input. Please enter a number from "
              + str(low) + " to " + str(high) + ".")


def parse_row_choice(text, total_rows):
    """
    Turn the typed text into how many rows to show.
    Enter gives 0, 'all' gives total_rows, a valid number gives that number.
    Anything else gives None (invalid).
    """
    assert total_rows > 0
    text = text.strip().lower()
    if text == "":
        return 0
    if text == "all":
        return total_rows
    if text.isdigit() and 1 <= int(text) <= total_rows:
        return int(text)
    return None


def parse_number_list(text, option_count, allow_empty):
    """
    Turn text like "1, 3" into the list [1, 3].
    Returns None if the text is not valid. A number that is typed twice
    is only kept once.
    """
    text = text.strip()
    if text == "":
        if allow_empty:
            return []
        return None

    numbers = []
    for part in text.split(","):
        part = part.strip()
        if not part.isdigit():
            return None
        number = int(part)
        if number < 1 or number > option_count:
            return None
        if number not in numbers:
            numbers.append(number)
    return numbers


def choose_options(title, options, allow_empty, end_text):
    # Show a numbered list. Return the names the user picked.
    while True:
        print("\n" + title)
        for number, option in enumerate(options, start=1):
            print(str(number) + ". " + option)
        text = input("Enter the number(s) of your choice(s), separated by "
                     "commas" + end_text + ": ")
        chosen_numbers = parse_number_list(text, len(options), allow_empty)
        if chosen_numbers is not None:
            chosen_names = []
            for number in chosen_numbers:
                chosen_names.append(options[number - 1])
            return chosen_names
        print("Invalid input. Use the numbers shown, separated by commas.")


def format_pivot(pivot):
    # Return the pivot table as text, rounded to 2 decimal places.
    return pivot.round(2).to_string()


def side_by_side(left_title, left_table, right_title, right_table, gap=6):
    # Return text that shows two tables next to each other.
    # Step 1: turn each table into a list of text lines.
    # Step 2: make every left line the same width.
    # Step 3: join each left line with the right line in the same position.
    left_lines = [left_title, "-" * len(left_title)]
    left_lines = left_lines + format_pivot(left_table).split("\n")
    right_lines = [right_title, "-" * len(right_title)]
    right_lines = right_lines + format_pivot(right_table).split("\n")

    # Find the longest left line.
    left_width = 0
    for line in left_lines:
        if len(line) > left_width:
            left_width = len(line)

    # Use the number of lines in the taller table.
    line_count = len(left_lines)
    if len(right_lines) > line_count:
        line_count = len(right_lines)

    combined = []
    for index in range(line_count):
        left = ""
        if index < len(left_lines):
            left = left_lines[index]
        right = ""
        if index < len(right_lines):
            right = right_lines[index]
        combined.append((left.ljust(left_width) + " " * gap + right).rstrip())
    return "\n".join(combined)


def show_first_rows(data):
    # Menu 1: show the first n rows.
    assert isinstance(data, pd.DataFrame)
    total_rows = len(data)

    while True:
        print("Enter rows to display:")
        print("- Enter a number 1 to " + str(total_rows))
        print("- To see all rows, enter 'all'")
        print("- To skip preview, press Enter")
        rows_to_show = parse_row_choice(input("Your choice: "), total_rows)
        if rows_to_show is not None:
            break
        print("Invalid input. Please try again.\n")

    if rows_to_show > 0:
        print(data.head(rows_to_show).to_string())
    return None


def total_sales_by_region_and_order_type(data):
    # Menu 2: total sales for each region, with a column for each order type.
    if not require_columns(data, [COL_REGION, COL_ORDER_TYPE, COL_PRICE]):
        return None
    return pd.pivot_table(
        data, index=COL_REGION, columns=COL_ORDER_TYPE, values=COL_PRICE,
        aggfunc="sum", fill_value=0, margins=True, margins_name="Total",
    )


def average_sales_by_region_state_and_order_type(data):
    # Menu 3: average sales for each region, split by state and order type.
    if not require_columns(data, [COL_REGION, COL_STATE, COL_ORDER_TYPE,
                                  COL_PRICE]):
        return None
    return pd.pivot_table(
        data, index=COL_REGION, columns=[COL_STATE, COL_ORDER_TYPE],
        values=COL_PRICE, aggfunc="mean", fill_value=0,
    )


def sales_by_customer_and_order_type_by_state(data):
    # Menu 4: sales for each state, split by customer type and order type.
    if not require_columns(data, [COL_STATE, COL_CUSTOMER_TYPE,
                                  COL_ORDER_TYPE, COL_PRICE]):
        return None
    return pd.pivot_table(
        data, index=[COL_STATE, COL_CUSTOMER_TYPE, COL_ORDER_TYPE],
        values=COL_PRICE, aggfunc="sum", fill_value=0,
    )


def quantity_and_price_by_region_and_product(data):
    # Menu 5: total quantity and total price for each region and product.
    if not require_columns(data, [COL_REGION, COL_PRODUCT, COL_QUANTITY,
                                  COL_PRICE]):
        return None
    return pd.pivot_table(
        data, index=[COL_REGION, COL_PRODUCT],
        values=[COL_QUANTITY, COL_PRICE], aggfunc="sum", fill_value=0,
    )[[COL_QUANTITY, COL_PRICE]]


def quantity_and_price_by_order_and_customer_type(data):
    # Menu 6: total quantity and total price for each order and customer type.
    if not require_columns(data, [COL_ORDER_TYPE, COL_CUSTOMER_TYPE,
                                  COL_QUANTITY, COL_PRICE]):
        return None
    return pd.pivot_table(
        data, index=[COL_ORDER_TYPE, COL_CUSTOMER_TYPE],
        values=[COL_QUANTITY, COL_PRICE], aggfunc="sum", fill_value=0,
    )[[COL_QUANTITY, COL_PRICE]]


def max_and_min_price_by_category(data):
    # Menu 7: highest and lowest sale price in each category.
    if not require_columns(data, [COL_CATEGORY, COL_PRICE]):
        return None
    return pd.pivot_table(
        data, index=COL_CATEGORY, values=COL_PRICE,
        aggfunc=["max", "min"], fill_value=0,
    )


def unique_employees_by_region(data):
    # Menu 8: how many different employees sold in each region.
    if not require_columns(data, [COL_REGION, COL_EMPLOYEE]):
        return None
    pivot = pd.pivot_table(
        data, index=COL_REGION, values=COL_EMPLOYEE, aggfunc="nunique",
    )
    return pivot.rename(columns={COL_EMPLOYEE: "unique_employees"})


def create_custom_pivot(data):
    # Menu 9: the user picks rows, columns, values and a function.
    assert isinstance(data, pd.DataFrame)

    # Only offer fields that are really in the data.
    row_options = []
    for name in PIVOT_ROW_CHOICES:
        if name in data.columns:
            row_options.append(name)
    column_options = []
    for name in PIVOT_COLUMN_CHOICES:
        if name in data.columns:
            column_options.append(name)
    value_options = []
    for name in PIVOT_VALUE_CHOICES:
        if name in data.columns:
            value_options.append(name)

    if len(row_options) == 0 or len(value_options) == 0:
        print("The data does not have enough fields for a custom pivot table.")
        return None

    rows = choose_options("Select rows:", row_options, False, "")
    columns = []
    if len(column_options) > 0:
        columns = choose_options("Select columns (optional):", column_options,
                                 True, " (enter for no grouping)")
    values = choose_options("Select values:", value_options, False, "")
    functions = choose_options("Select aggregation function:",
                               PIVOT_AGGREGATIONS, False, "")

    # A field cannot be used as both a row and a column.
    overlap = []
    for name in rows:
        if name in columns:
            overlap.append(name)
    if len(overlap) > 0:
        print("A field cannot be used as both a row and a column: "
              + ", ".join(overlap))
        return None

    # pandas needs None (not an empty list) when there are no columns.
    column_setting = None
    if len(columns) > 0:
        column_setting = columns

    try:
        return pd.pivot_table(
            data, index=rows, columns=column_setting,
            values=values, aggfunc=functions, fill_value=0,
        )
    except (ValueError, KeyError, TypeError) as error:
        print("Could not build the pivot table: " + str(error))
        return None


def percent_of_region_by_product(data):
    # Menu 10 (individual task 2): quantity and sales for each region and
    # product, plus two new columns showing each row as a percent of its region.
    if not require_columns(data, [COL_REGION, COL_PRODUCT, COL_QUANTITY,
                                  COL_PRICE]):
        return None

    totals = pd.pivot_table(
        data, index=[COL_REGION, COL_PRODUCT],
        values=[COL_QUANTITY, COL_PRICE], aggfunc="sum", fill_value=0,
    )[[COL_QUANTITY, COL_PRICE]]

    # groupby(level=0) groups the rows by region.
    # transform("sum") puts the region's total on every row of that region.
    # So: row value / region total * 100 = percent of the region.
    region_totals = totals.groupby(level=0).transform("sum")
    percents = totals / region_totals * 100

    # If a region's total is 0, the math gives "not a number". Show 0 instead.
    percents = percents.fillna(0).round(2)

    totals["pct_of_region_quantity"] = percents[COL_QUANTITY]
    totals["pct_of_region_sales"] = percents[COL_PRICE]
    return totals


def get_comparable_items():
    # Return a dictionary like {menu number: (label, function)} with only the
    # menu items that return a table. Only those can be compared.
    comparable = {}
    number = 1
    for item in MENU_ITEMS:
        label = item[0]
        function = item[1]
        if function not in NON_TABLE_FUNCTIONS:
            comparable[number] = (label, function)
        number = number + 1
    return comparable


def choose_comparable_item(comparable, prompt):
    # Keep asking until the user types a menu number that can be compared.
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) in comparable:
            return comparable[int(text)]
        print("Invalid input. Choose one of the numbers listed above.")


def compare_analytics(data):
    # Menu 11 (individual task 1): show two analyses side by side.
    assert isinstance(data, pd.DataFrame)
    comparable = get_comparable_items()

    print("Analytics you can compare:")
    for number in comparable:
        print(str(number) + ". " + comparable[number][0])

    first = choose_comparable_item(
        comparable, "Enter the number of the FIRST analytic: ")
    second = choose_comparable_item(
        comparable, "Enter the number of the SECOND analytic: ")

    # Each function returns its table, so we can keep both and print them
    # together. first[1] is the function of the first choice.
    left_table = first[1](data)
    right_table = second[1](data)
    if left_table is None or right_table is None:
        print("One of the analytics could not be produced, "
              "so there is nothing to compare.")
        return None

    print()
    print(side_by_side(first[0], left_table, second[0], right_table))
    return None


def exit_dashboard(data):
    # Menu 12: say goodbye. The menu loop does the actual stopping.
    print("Goodbye!")
    return None

MENU_ITEMS = [
    ("Show the first n rows of sales data", show_first_rows),
    ("Total sales by region and order_type",
     total_sales_by_region_and_order_type),
    ("Average sales by region with average sales by state and sale type",
     average_sales_by_region_state_and_order_type),
    ("Sales by customer type and order type by state",
     sales_by_customer_and_order_type_by_state),
    ("Total sales quantity and price by region and product",
     quantity_and_price_by_region_and_product),
    ("Total sales quantity and price by customer type",
     quantity_and_price_by_order_and_customer_type),
    ("Max and min sales price of sales by category",
     max_and_min_price_by_category),
    ("Number of unique employees by region", unique_employees_by_region),
    ("Create a custom pivot table", create_custom_pivot),
    ("Percent of region quantity and sales by region and product",
     percent_of_region_by_product),
    ("Compare two analytics side by side", compare_analytics),
    ("Exit", exit_dashboard),
]

# These menu items do not return a table, so they cannot be compared.
NON_TABLE_FUNCTIONS = [show_first_rows, compare_analytics, exit_dashboard]


def show_menu(menu_items):
    # Print the numbered menu.
    print("\n--- Sales Data Dashboard ---")
    number = 1
    for item in menu_items:
        print(str(number) + ". " + item[0])
        number = number + 1


def run_menu(data, menu_items=MENU_ITEMS):
    # Show the menu again and again until the user picks Exit.
    while True:
        show_menu(menu_items)
        choice = read_int_in_range("Enter your choice: ", 1, len(menu_items))
        label = menu_items[choice - 1][0]
        function = menu_items[choice - 1][1]

        print("\n=== " + label + " ===")
        result = function(data)
        if result is not None:
            print(format_pivot(result))

        if function == exit_dashboard:
            break


def main():
    # Load the data, show information about it, then start the menu.
    print("Loading sales data from Google Drive...")
    data, seconds, error_message = load_sales_data(DATA_URL, LOCAL_FILE_NAME)

    if error_message != "":
        print("ERROR: " + error_message)
        print("The dashboard cannot start without the data. Exiting.")
        sys.exit(1)

    print("File loaded successfully.")
    print("Load time: " + format(seconds, ".2f") + " seconds")
    print("Rows of data: " + str(len(data)))
    print("Available columns: " + ", ".join(data.columns))

    missing = missing_columns(data, REQUIRED_COLUMNS)
    if len(missing) > 0:
        print("\nWARNING: These expected columns are missing: "
              + ", ".join(missing))
        print("Some analytics will not work.")

    # EOFError and KeyboardInterrupt happen when the user closes the input
    # or presses Ctrl+C. We exit instead of showing an error.
    try:
        run_menu(data)
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Goodbye!")


if __name__ == "__main__":
    main()
