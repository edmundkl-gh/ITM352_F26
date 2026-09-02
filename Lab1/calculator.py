"""
Simple Calculator Program
Performs basic math operations: add, subtract, multiply, divide
Includes error handling for division by zero
"""

def add(x, y):
    """Add two numbers"""
    return x + y

def subtract(x, y):
    """Subtract two numbers"""
    return x - y

def multiply(x, y):
    """Multiply two numbers"""
    return x * y

def divide(x, y):
    """Divide two numbers with zero division check"""
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

def calculator():
    """Main calculator function"""
    while True:
        print("=" * 40)
        print("         SIMPLE CALCULATOR")
        print("=" * 40)

        try:
            # Get user input for two numbers
            num1 = float(input("\nEnter first number: "))
            num2 = float(input("Enter second number: "))

            # Display operation options
            print("\nSelect an operation:")
            print("1. Add (+)")
            print("2. Subtract (-)")
            print("3. Multiply (*)")
            print("4. Divide (/)")

            # Get user's operation choice
            choice = input("\nEnter your choice (1/2/3/4): ")

            # Perform the selected operation
            if choice == '1':
                result = add(num1, num2)
                operation = "+"
            elif choice == '2':
                result = subtract(num1, num2)
                operation = "-"
            elif choice == '3':
                result = multiply(num1, num2)
                operation = "*"
            elif choice == '4':
                result = divide(num1, num2)
                operation = "/"
            else:
                print("Invalid choice! Please select 1, 2, 3, or 4.")
                again = input("\nWould you like to do another calculation? (y/n): ").strip().lower()
                if again != 'y':
                    print("Goodbye!")
                    return
                continue

            # Display the result
            print("\n" + "=" * 40)
            print(f"Result: {num1} {operation} {num2} = {result}")
            print("=" * 40)

        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

        again = input("\nWould you like to do another calculation? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            return

if __name__ == "__main__":
    calculator()
