```python
# solutions.py

def check_even_or_odd(number):
    """
    This function checks if a number is even or odd.

    Args:
        number (int): The number to be checked.

    Returns:
        str: A message indicating whether the number is even or odd.
    """
    if number % 2 == 0:
        return f"{number} is even."
    else:
        return f"{number} is odd."


def main():
    # Example usage:
    numbers = [10, 23, 44, 57, 92]

    for number in numbers:
        print(check_even_or_odd(number))


if __name__ == "__main__":
    main()
```