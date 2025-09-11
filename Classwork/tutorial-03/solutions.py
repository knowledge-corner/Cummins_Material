```python
# solutions.py

def calculate_factorial(n):
    """
    Calculate the factorial of a given integer.

    Args:
        n (int): The input number.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is a negative number.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def calculate_factorial_recursive(n):
    """
    Calculate the factorial of a given integer using recursion.

    Args:
        n (int): The input number.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is a negative number.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial_recursive(n - 1)


def main():
    # Test the functions
    numbers = [0, 1, 2, 3, 4, 5]
    for num in numbers:
        print(f"Factorial of {num} (iterative): {calculate_factorial(num)}")
        print(f"Factorial of {num} (recursive): {calculate_factorial_recursive(num)}")


if __name__ == "__main__":
    main()
```