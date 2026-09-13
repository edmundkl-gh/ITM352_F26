#Create a function called apply that take in two numbers and a function as parameters and return the result
#Edmund Liu
#Sept. 12, 2026

def apply(x, y, func):
    return f"The function {func.__name__} {x},{y} = {func(x, y)}"