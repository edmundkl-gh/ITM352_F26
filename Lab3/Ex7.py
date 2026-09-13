# Temperature conversion functions using a passed-in conversion function
# Edmund Liu
# Sept. 12, 2026

def c_to_f(celsius):
    return (celsius * 9 / 5) + 32


def f_to_c(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def c_to_k(celsius):
    return celsius + 273.15


def k_to_c(kelvin):
    return kelvin - 273.15


def f_to_k(fahrenheit):
    return c_to_k(f_to_c(fahrenheit))


def k_to_f(kelvin):
    return c_to_f(k_to_c(kelvin))


def apply(value, conversion_func):
    return conversion_func(value)


if __name__ == "__main__":
    print(apply(0, c_to_f))
    print(apply(32, f_to_c))
    print(apply(100, c_to_k))
    print(apply(273.15, k_to_c))