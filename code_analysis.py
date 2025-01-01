import ast
import math


def unsafe_function(user_input):
    try:
        result = ast.literal_eval(user_input)
        print(f"Result:  {result}")
    except NameError:
        print("Invalid Input")

    # Potential vulnerability: Unchecked input
    eval(user_input)  # Risk of code injection
    print("User input evaluated.")


user_input = input("Enter something: ")
unsafe_function(user_input)


def calculate_area(radius):
    # Vulnerable to floating-point precision issues
    area = math.pi * radius * radius
    print(f"Area of circle with radius {radius}: {area}")
    return area


def main():
    radius = float(input("Enter the radius: "))
    calculate_area(radius)


if __name__ == "__main__":
    main()
