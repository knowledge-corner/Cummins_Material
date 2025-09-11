```python
# solutions.py

def calculate_factorial(n):
    """
    Calculate the factorial of a given number.

    Args:
    n (int): The number to calculate the factorial for.

    Returns:
    int: The factorial of the given number.

    Raises:
    ValueError: If the input number is negative.
    """

    # Check if the input number is negative
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")

    # Base case: factorial of 0 or 1 is 1
    elif n == 0 or n == 1:
        return 1

    # Calculate the factorial using recursion
    else:
        return n * calculate_factorial(n-1)


def calculate_factorial_iterative(n):
    """
    Calculate the factorial of a given number using iteration.

    Args:
    n (int): The number to calculate the factorial for.

    Returns:
    int: The factorial of the given number.

    Raises:
    ValueError: If the input number is negative.
    """

    # Check if the input number is negative
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")

    # Initialize the result variable
    result = 1

    # Calculate the factorial using iteration
    for i in range(1, n + 1):
        result *= i

    return result


def main():
    # Example usage
    num = 5
    print(f"Factorial of {num} using recursion: {calculate_factorial(num)}")
    print(f"Factorial of {num} using iteration: {calculate_factorial_iterative(num)}")


if __name__ == "__main__":
    main()
```