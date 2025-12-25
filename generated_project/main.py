#!/usr/bin/env python3
"""Main application file that takes two integers as input and returns their difference."""

from calculator import calculate_difference


def diff_numbers(a, b):
    """Calculate the difference between two numbers with type validation.
    
    Args:
        a: The first number (must be int or float)
        b: The second number (must be int or float)
    
    Returns:
        The difference (a - b)
    
    Raises:
        ValueError: If inputs are not valid numbers
    """
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        raise ValueError("First argument must be a number")
    if not isinstance(b, (int, float)) or isinstance(b, bool) or b is None:
        raise ValueError("Second argument must be a number")
    
    return a - b


def main():
    """Main function to get user input and display the difference."""
    try:
        num1 = int(input("Enter the first integer: "))
        num2 = int(input("Enter the second integer: "))
        
        result = diff_numbers(num1, num2)
        
        print(f"{num1} - {num2} = {result}")
    
    except ValueError as e:
        if "invalid literal" in str(e):
            print("Error: Please enter valid integers.")
        else:
            raise
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
