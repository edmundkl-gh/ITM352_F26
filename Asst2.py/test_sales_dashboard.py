"""
test_sales_dashboard_basic.py - Tests for sales_dashboard_basic.py

Run with:   python test_sales_dashboard_basic.py

HOW IT WORKS
* check(description, condition) prints PASS or FAIL and counts the results.
* The tests use a small table with 5 rows, so the right answers are easy to
  work out by hand. The numbers are listed in build_sample_data().
* The dashboard asks the user questions with input(). In the tests we swap
  input() for fake_input(), which gives answers from a prepared list.
  This lets the tests "type" for us.
* We also catch what the dashboard prints, so we can check its messages.
"""

import io
import os
import sys

import pandas as pd

import sales_dashboard_basic as sd

TEMP_FILE = "test_temp_sales.csv"
passed_count = 0
failed_count = 0


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------
def check(description, condition):
    """Print PASS or FAIL for one check and count it."""
    global passed_count, failed_count
    if condition:
        passed_count = passed_count + 1
        print("PASS: " + description)
    else:
        failed_count = failed_count + 1
        print("FAIL: " + description)


def build_sample_data():
    """Return a small table with 5 rows and known totals.

    East: Ann sold Widget (qty 2, $10 Retail) and Gadget (qty 3, $30 Wholesale)
    West: Bob sold Widget (qty 1, $20 Retail) and Gizmo (qty 5, $60 Wholesale)
          Cara sold Gizmo (qty 4, $40 Retail)
    """
    return pd.DataFrame({
        sd.COL_REGION: ["East", "East", "West", "West", "West"],
        sd.COL_STATE: ["HI", "HI", "CA", "CA", "NV"],
        sd.COL_ORDER_TYPE: ["Retail", "Wholesale", "Retail", "Retail",
                            "Wholesale"],
        sd.COL_CUSTOMER_TYPE: ["Business", "Business", "Individual",
                               "Individual", "Business"],
        sd.COL_PRODUCT: ["Widget", "Gadget", "Widget", "Gizmo", "Gizmo"],
        sd.COL_CATEGORY: ["Hardware", "Hardware", "Hardware", "Software",
                          "Software"],
        sd.COL_QUANTITY: [2, 3, 1, 4, 5],
        sd.COL_PRICE: [10, 30, 20, 40, 60],
        sd.COL_EMPLOYEE: ["Ann", "Ann", "Bob", "Cara", "Bob"],
    })


# --- fake keyboard input ---------------------------------------------------
fake_answers = []


def fake_input(prompt):
    """Pretend to be input(): give back the next prepared answer."""
    return fake_answers.pop(0)


def end_of_input(prompt):
    """Pretend the user closed the input (Ctrl+D)."""
    raise EOFError


def set_answers(answers):
    """Set the answers that the next input() calls will receive."""
    fake_answers.clear()
    for answer in answers:
        fake_answers.append(answer)


# From now on, the dashboard uses fake_input instead of the real input().
sd.input = fake_input


# --- capturing printed text ------------------------------------------------
real_stdout = sys.stdout
capture_buffer = io.StringIO()


def start_capture():
    """Start saving printed text instead of showing it."""
    global capture_buffer
    capture_buffer = io.StringIO()
    sys.stdout = capture_buffer


def stop_capture():
    """Show printed text again and return what was saved."""
    sys.stdout = real_stdout
    return capture_buffer.getvalue()


def write_temp_file(text):
    """Create a small text file for the loading tests."""
    file = open(TEMP_FILE, "w")
    file.write(text)
    file.close()


def remove_temp_files():
    """Delete the files the tests created."""
    for name in [TEMP_FILE, "test_copy.csv"]:
        if os.path.exists(name):
            os.remove(name)


# ---------------------------------------------------------------------------
# Tests: loading and cleaning
# ---------------------------------------------------------------------------
def test_loading_and_cleaning():
    print("\n--- Loading and cleaning ---")

    # A good file
    build_sample_data().to_csv(TEMP_FILE, index=False)
    data, seconds, error = sd.load_sales_data(TEMP_FILE, "test_copy.csv")
    check("good file loads with no error", error == "")
    check("good file has 5 rows", len(data) == 5)
    check("load time is not negative", seconds >= 0)
    check("a local copy was saved", os.path.exists("test_copy.csv"))

    # Bad files
    data, seconds, error = sd.load_sales_data("no_such_file.csv", "x.csv")
    check("missing file gives an error message", error != "")
    check("missing file gives no data", data is None)

    write_temp_file("")
    data, seconds, error = sd.load_sales_data(TEMP_FILE, "x.csv")
    check("empty file gives an error message", error != "")

    write_temp_file("a,b,c\n")
    data, seconds, error = sd.load_sales_data(TEMP_FILE, "x.csv")
    check("header-only file gives an error message", error != "")

    write_temp_file("<html>Sign in to Google</html>\n")
    data, seconds, error = sd.load_sales_data(TEMP_FILE, "x.csv")
    check("web page instead of a CSV gives an error message", error != "")

    # Cleaning the data
    messy = build_sample_data()
    messy.loc[0, sd.COL_PRICE] = None
    messy.loc[1, sd.COL_EMPLOYEE] = None
    cleaned = sd.clean_data(messy)
    check("missing number becomes 0", cleaned.loc[0, sd.COL_PRICE] == 0)
    check("missing text becomes 0", cleaned.loc[1, sd.COL_EMPLOYEE] == 0)
    check("clean_data leaves the original alone",
          pd.isna(messy.loc[0, sd.COL_PRICE]))

    bad_numbers = build_sample_data()
    bad_numbers[sd.COL_QUANTITY] = bad_numbers[sd.COL_QUANTITY].astype(object)
    bad_numbers.loc[2, sd.COL_QUANTITY] = "abc"
    check("text in a number column becomes 0",
          sd.clean_data(bad_numbers).loc[2, sd.COL_QUANTITY] == 0)

    spaced = build_sample_data().rename(columns={sd.COL_PRICE: " sale_price "})
    check("spaces around column names are removed",
          sd.COL_PRICE in sd.clean_data(spaced).columns)


def test_column_checks():
    print("\n--- Column checks ---")
    data = build_sample_data()
    check("no columns missing from full data",
          sd.missing_columns(data, sd.REQUIRED_COLUMNS) == [])

    smaller = data.drop(columns=[sd.COL_PRICE])
    check("finds the missing column",
          sd.missing_columns(smaller, sd.REQUIRED_COLUMNS) == [sd.COL_PRICE])

    check("require_columns True when present",
          sd.require_columns(data, [sd.COL_REGION]) == True)
    start_capture()
    answer = sd.require_columns(smaller, [sd.COL_PRICE])
    text = stop_capture()
    check("require_columns False when missing", answer == False)
    check("require_columns names the missing column", "sale_price" in text)


# ---------------------------------------------------------------------------
# Tests: input helpers
# ---------------------------------------------------------------------------
def test_input_helpers():
    print("\n--- Input helpers ---")

    set_answers(["abc", "0", "13", "", "5"])
    start_capture()
    number = sd.read_int_in_range("Pick: ", 1, 12)
    text = stop_capture()
    check("read_int_in_range returns the first valid number", number == 5)
    check("read_int_in_range rejects bad input", "Invalid input" in text)

    check("Enter means skip (0 rows)", sd.parse_row_choice("", 10) == 0)
    check("'all' means every row", sd.parse_row_choice("all", 10) == 10)
    check("'ALL' with spaces works", sd.parse_row_choice(" ALL ", 10) == 10)
    check("1 is valid", sd.parse_row_choice("1", 10) == 1)
    check("the last row number is valid", sd.parse_row_choice("10", 10) == 10)
    for bad in ["0", "11", "-3", "2.5", "some", "1,2"]:
        check("parse_row_choice rejects '" + bad + "'",
              sd.parse_row_choice(bad, 10) is None)

    check("number list '1, 3'", sd.parse_number_list("1, 3", 3, False) == [1, 3])
    check("repeated numbers ignored",
          sd.parse_number_list("2,2", 3, False) == [2])
    check("empty is OK when allowed", sd.parse_number_list("", 3, True) == [])
    check("empty rejected when not allowed",
          sd.parse_number_list("", 3, False) is None)
    check("too big rejected", sd.parse_number_list("4", 3, False) is None)
    check("zero rejected", sd.parse_number_list("0", 3, False) is None)
    check("letters rejected", sd.parse_number_list("a", 3, False) is None)
    check("blank piece rejected", sd.parse_number_list("1,,2", 3, False) is None)

    set_answers(["2,1"])
    start_capture()
    names = sd.choose_options("Pick:", ["a", "b", "c"], False, "")
    stop_capture()
    check("choose_options returns the names", names == ["b", "a"])

    set_answers(["9", "x", "3"])
    start_capture()
    names = sd.choose_options("Pick:", ["a", "b", "c"], False, "")
    text = stop_capture()
    check("choose_options retries after bad input", names == ["c"])
    check("choose_options shows an error", "Invalid input" in text)

    set_answers([""])
    start_capture()
    names = sd.choose_options("Pick:", ["a", "b"], True, "")
    stop_capture()
    check("choose_options allows empty when optional", names == [])


def test_output_helpers():
    print("\n--- Output helpers ---")
    table = pd.DataFrame({"x": [1234.5678]})
    check("format_pivot rounds to 2 decimals",
          "1234.57" in sd.format_pivot(table))

    left = pd.DataFrame({"a": [1, 2, 3]})
    right = pd.DataFrame({"b": [9]})
    lines = sd.side_by_side("LEFT", left, "RIGHT", right).split("\n")
    check("side_by_side first line has both titles",
          "LEFT" in lines[0] and "RIGHT" in lines[0])
    check("side_by_side has as many lines as the taller table",
          len(lines) == 2 + 1 + 3)


# ---------------------------------------------------------------------------
# Tests: analytics
# ---------------------------------------------------------------------------
def test_analytics():
    print("\n--- Analytics ---")
    data = build_sample_data()

    result = sd.total_sales_by_region_and_order_type(data)
    check("total: East Retail = 10", result.loc["East", "Retail"] == 10)
    check("total: East Wholesale = 30", result.loc["East", "Wholesale"] == 30)
    check("total: West Retail = 60", result.loc["West", "Retail"] == 60)
    check("total: West Wholesale = 60", result.loc["West", "Wholesale"] == 60)
    check("total: grand total = 160", result.loc["Total", "Total"] == 160)

    result = sd.average_sales_by_region_state_and_order_type(data)
    check("average: East HI Retail = 10",
          result.loc["East", ("HI", "Retail")] == 10)
    check("average: West CA Retail = 30",
          result.loc["West", ("CA", "Retail")] == 30)
    check("average: West NV Wholesale = 60",
          result.loc["West", ("NV", "Wholesale")] == 60)
    check("average: empty combination is 0",
          result.loc["East", ("CA", "Retail")] == 0)

    result = sd.sales_by_customer_and_order_type_by_state(data)
    check("by state: CA Individual Retail = 60",
          result.loc[("CA", "Individual", "Retail"), sd.COL_PRICE] == 60)
    check("by state: HI Business Wholesale = 30",
          result.loc[("HI", "Business", "Wholesale"), sd.COL_PRICE] == 30)

    result = sd.quantity_and_price_by_region_and_product(data)
    check("region/product: West Gizmo quantity = 9",
          result.loc[("West", "Gizmo"), sd.COL_QUANTITY] == 9)
    check("region/product: West Gizmo price = 100",
          result.loc[("West", "Gizmo"), sd.COL_PRICE] == 100)
    check("region/product: columns in the right order",
          list(result.columns) == [sd.COL_QUANTITY, sd.COL_PRICE])

    result = sd.quantity_and_price_by_order_and_customer_type(data)
    check("customer type: Retail Individual quantity = 5",
          result.loc[("Retail", "Individual"), sd.COL_QUANTITY] == 5)
    check("customer type: Retail Individual price = 60",
          result.loc[("Retail", "Individual"), sd.COL_PRICE] == 60)
    check("customer type: Wholesale Business price = 90",
          result.loc[("Wholesale", "Business"), sd.COL_PRICE] == 90)

    result = sd.max_and_min_price_by_category(data)
    check("max/min: Hardware max = 30",
          result.loc["Hardware", ("max", sd.COL_PRICE)] == 30)
    check("max/min: Hardware min = 10",
          result.loc["Hardware", ("min", sd.COL_PRICE)] == 10)
    check("max/min: Software max = 60",
          result.loc["Software", ("max", sd.COL_PRICE)] == 60)
    check("max/min: Software min = 40",
          result.loc["Software", ("min", sd.COL_PRICE)] == 40)

    result = sd.unique_employees_by_region(data)
    check("unique employees: East = 1",
          result.loc["East", "unique_employees"] == 1)
    check("unique employees: West = 2",
          result.loc["West", "unique_employees"] == 2)


def test_percent_analytic():
    print("\n--- Percent of region analytic ---")
    data = build_sample_data()
    result = sd.percent_of_region_by_product(data)

    check("East Gadget quantity is 60%",
          result.loc[("East", "Gadget"), "pct_of_region_quantity"] == 60.0)
    check("East Gadget sales is 75%",
          result.loc[("East", "Gadget"), "pct_of_region_sales"] == 75.0)
    check("West Gizmo quantity is 90%",
          result.loc[("West", "Gizmo"), "pct_of_region_quantity"] == 90.0)
    check("West Gizmo sales is 83.33%",
          result.loc[("West", "Gizmo"), "pct_of_region_sales"] == 83.33)

    sums = result.groupby(level=0)[["pct_of_region_quantity",
                                    "pct_of_region_sales"]].sum()
    check("East percentages add up to about 100",
          abs(sums.loc["East", "pct_of_region_quantity"] - 100) < 0.1)
    check("West percentages add up to about 100",
          abs(sums.loc["West", "pct_of_region_sales"] - 100) < 0.1)

    data[sd.COL_QUANTITY] = 0
    result = sd.percent_of_region_by_product(data)
    check("region total of 0 gives 0%, not an error",
          result["pct_of_region_quantity"].sum() == 0)


def test_missing_columns_in_analytics():
    print("\n--- Analytics with missing columns ---")
    unrelated = pd.DataFrame({"unrelated": [1, 2]})
    analytics = [
        sd.total_sales_by_region_and_order_type,
        sd.average_sales_by_region_state_and_order_type,
        sd.sales_by_customer_and_order_type_by_state,
        sd.quantity_and_price_by_region_and_product,
        sd.quantity_and_price_by_order_and_customer_type,
        sd.max_and_min_price_by_category,
        sd.unique_employees_by_region,
        sd.percent_of_region_by_product,
    ]
    for analytic in analytics:
        start_capture()
        result = analytic(unrelated)
        text = stop_capture()
        check(analytic.__name__ + " returns None and explains why",
              result is None and "Missing" in text)


# ---------------------------------------------------------------------------
# Tests: menu 1 and menu 9
# ---------------------------------------------------------------------------
def test_show_first_rows():
    print("\n--- Show first rows ---")
    data = build_sample_data()

    set_answers(["2"])
    start_capture()
    result = sd.show_first_rows(data)
    text = stop_capture()
    check("returns None", result is None)
    check("shows the first rows", "Ann" in text)
    check("does not show later rows", "Cara" not in text)

    set_answers(["all"])
    start_capture()
    sd.show_first_rows(data)
    text = stop_capture()
    check("'all' shows every row", "Cara" in text)

    set_answers([""])
    start_capture()
    sd.show_first_rows(data)
    text = stop_capture()
    check("Enter skips the preview", "Ann" not in text)
    check("tells the user how many rows exist", "1 to 5" in text)

    set_answers(["0", "6", "abc", "1"])
    start_capture()
    sd.show_first_rows(data)
    text = stop_capture()
    check("three invalid answers are rejected", text.count("Invalid input") == 3)
    check("then the valid answer works", "Ann" in text)


def test_custom_pivot():
    print("\n--- Custom pivot ---")
    data = build_sample_data()

    # Choices typed: rows = sales_region (2), columns = order_type (1),
    # values = sale_price (2), function = sum (1)
    set_answers(["2", "1", "2", "1"])
    start_capture()
    result = sd.create_custom_pivot(data)
    stop_capture()
    check("custom: East Retail sum = 10",
          result.loc["East", ("sum", sd.COL_PRICE, "Retail")] == 10)
    check("custom: West Wholesale sum = 60",
          result.loc["West", ("sum", sd.COL_PRICE, "Wholesale")] == 60)

    # A bad answer first, then no columns
    set_answers(["x", "2", "", "2", "1"])
    start_capture()
    result = sd.create_custom_pivot(data)
    stop_capture()
    check("custom without columns: East = 40",
          result.loc["East", ("sum", sd.COL_PRICE)] == 40)
    check("custom without columns: West = 120",
          result.loc["West", ("sum", sd.COL_PRICE)] == 120)

    # Two values and two functions (sum and count)
    set_answers(["2", "", "1,2", "1,3"])
    start_capture()
    result = sd.create_custom_pivot(data)
    stop_capture()
    check("custom: West count = 3",
          result.loc["West", ("count", sd.COL_QUANTITY)] == 3)
    check("custom: West quantity sum = 10",
          result.loc["West", ("sum", sd.COL_QUANTITY)] == 10)

    start_capture()
    result = sd.create_custom_pivot(data[[sd.COL_REGION]])
    text = stop_capture()
    check("custom: not enough fields gives a message",
          result is None and "not have enough fields" in text)


# ---------------------------------------------------------------------------
# Tests: compare and menu
# ---------------------------------------------------------------------------
def test_compare():
    print("\n--- Compare side by side ---")
    data = build_sample_data()

    comparable = sd.get_comparable_items()
    check("menu item 2 can be compared", 2 in comparable)
    check("menu item 1 cannot be compared", 1 not in comparable)
    check("Exit cannot be compared", len(sd.MENU_ITEMS) not in comparable)

    # 2 = total sales by region and order type, 8 = unique employees
    set_answers(["2", "8"])
    start_capture()
    result = sd.compare_analytics(data)
    text = stop_capture()
    check("compare returns None", result is None)
    check("first analytic title shown",
          "Total sales by region and order_type" in text)
    check("second analytic title shown",
          "Number of unique employees by region" in text)
    check("both tables shown", "Wholesale" in text and "unique_employees" in text)

    set_answers(["1", "abc", "2", "99", "8"])
    start_capture()
    sd.compare_analytics(data)
    text = stop_capture()
    check("invalid compare choices are rejected",
          text.count("Invalid input") == 3)

    set_answers(["2", "8"])
    start_capture()
    sd.compare_analytics(data.drop(columns=[sd.COL_EMPLOYEE]))
    text = stop_capture()
    check("compare explains when an analytic cannot run",
          "nothing to compare" in text)


def say_hi(data):
    """A tiny menu function for testing a custom menu."""
    return pd.DataFrame({"hi": [1]})


def test_menu():
    print("\n--- Menu ---")
    data = build_sample_data()

    labels = []
    all_valid = True
    for item in sd.MENU_ITEMS:
        labels.append(item[0])
        if type(item[0]) != str or not callable(item[1]):
            all_valid = False
    check("every menu item is (text, function)", all_valid)
    check("menu labels are unique", len(labels) == len(set(labels)))
    check("first item is show rows",
          labels[0] == "Show the first n rows of sales data")
    check("last item is Exit", labels[-1] == "Exit")
    check("custom pivot is in the menu", "Create a custom pivot table" in labels)

    set_answers(["12"])
    start_capture()
    sd.run_menu(data)
    text = stop_capture()
    check("Exit stops the menu", "Goodbye!" in text)

    set_answers(["2", "12"])
    start_capture()
    sd.run_menu(data)
    text = stop_capture()
    check("menu runs an analytic and prints its title",
          "=== Total sales by region and order_type ===" in text)
    check("menu prints the table", "160" in text)

    set_answers(["10", "12"])
    start_capture()
    sd.run_menu(data)
    text = stop_capture()
    check("menu runs the percent analytic", "pct_of_region_sales" in text)

    set_answers(["99", "abc", "", "12"])
    start_capture()
    sd.run_menu(data)
    text = stop_capture()
    check("invalid menu choices are rejected", text.count("Invalid input") == 3)

    # The menu should work with any list of (label, function) pairs.
    custom_menu = [("Say hi", say_hi), ("Exit", sd.exit_dashboard)]
    set_answers(["1", "2"])
    start_capture()
    sd.run_menu(data, custom_menu)
    text = stop_capture()
    check("a custom menu list works", "Say hi" in text)

    start_capture()
    result = sd.exit_dashboard(data)
    text = stop_capture()
    check("exit_dashboard says goodbye and returns None",
          result is None and "Goodbye" in text)


# ---------------------------------------------------------------------------
# Tests: main
# ---------------------------------------------------------------------------
def test_main():
    print("\n--- main ---")
    real_loader = sd.load_sales_data

    # Swap the loader for a fake one that fails.
    def failing_loader(source, copy_name):
        return None, 0, "boom"

    sd.load_sales_data = failing_loader
    start_capture()
    exit_code = None
    try:
        sd.main()
    except SystemExit as error:
        exit_code = error.code
    text = stop_capture()
    check("main exits with code 1 when loading fails", exit_code == 1)
    check("main prints the error", "ERROR: boom" in text)

    # Swap the loader for a fake one that works.
    def working_loader(source, copy_name):
        return build_sample_data(), 0.25, ""

    sd.load_sales_data = working_loader
    set_answers(["12"])
    start_capture()
    sd.main()
    text = stop_capture()
    check("main reports success", "loaded successfully" in text)
    check("main reports load time", "0.25 seconds" in text)
    check("main reports row count", "Rows of data: 5" in text)
    check("main lists columns", "sale_price" in text)
    check("main has no warning for complete data", "WARNING" not in text)

    def loader_missing_price(source, copy_name):
        return build_sample_data().drop(columns=[sd.COL_PRICE]), 0.1, ""

    sd.load_sales_data = loader_missing_price
    set_answers(["12"])
    start_capture()
    sd.main()
    text = stop_capture()
    check("main warns about missing columns",
          "WARNING" in text and "sale_price" in text)
    check("main says analytics may not work",
          "Some analytics will not work" in text)

    sd.load_sales_data = working_loader
    sd.input = end_of_input
    start_capture()
    sd.main()
    text = stop_capture()
    sd.input = fake_input
    check("main handles input ending", "Goodbye" in text)

    sd.load_sales_data = real_loader


# ---------------------------------------------------------------------------
# Run everything
# ---------------------------------------------------------------------------
def run_all_tests():
    test_loading_and_cleaning()
    test_column_checks()
    test_input_helpers()
    test_output_helpers()
    test_analytics()
    test_percent_analytic()
    test_missing_columns_in_analytics()
    test_show_first_rows()
    test_custom_pivot()
    test_compare()
    test_menu()
    test_main()
    remove_temp_files()

    print("\n==============================")
    print("Passed: " + str(passed_count))
    print("Failed: " + str(failed_count))


run_all_tests()
