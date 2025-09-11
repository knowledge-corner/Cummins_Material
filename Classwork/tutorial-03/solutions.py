```python
# solutions.py

def is_prime(n):
    """
    Checks if a number is prime.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max_divisor = int(n**0.5) + 1
    for d in range(3, max_divisor, 2):
        if n % d == 0:
            return False
    return True


def get_primes(n):
    """
    Generates a list of prime numbers up to n.

    Args:
        n (int): The upper limit.

    Returns:
        list: A list of prime numbers up to n.
    """
    primes = []
    for i in range(2, n + 1):
        if is_prime(i):
            primes.append(i)
    return primes


def main():
    # Example usage
    n = 100
    primes = get_primes(n)
    print(f"Prime numbers up to {n}: {primes}")


if __name__ == "__main__":
    main()
```