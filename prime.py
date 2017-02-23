import sys
import math
from datetime import date
from functools import reduce
from math import sqrt
from itertools import count, islice


def is_prime(num):
    """Determines if a number is prime."""
    # Credit to: http://stackoverflow.com/a/27946768/6465897
    return num > 1 and all(num % i for i in islice(count(2), int(sqrt(num)-1)))


def is_day_prime(day):
    """Determines if a datetime object is a prime day."""

    return is_prime(int(str(day).replace('-', '')))


def prime_factors(num):
    """Returns a tuple containing the prime factors of a specified num."""

    factors = ()
    if is_prime(num):
        return (num,)

    mid = num // 2  # Only need to check first half of numbers.
    for val in range(2, mid + 1):
        if num % val == 0:
            # Treat the quotient and the divisor as separate branches of a tree:
            # if either of these values are not prime, recurse down them until 
            # their prime factors are determined.
            result = num // val 

            # Do not allow duplicates to be added to the current iteration.
            if result in factors or val in factors:  
                continue
            if is_prime(val): 
                factors += (val,)
            else: 
                factors += prime_factors(val)
            if is_prime(result):
                factors += (result,)
            else:
                factors += prime_factors(result)
            if reduce(lambda x, y: x * y, factors) == num:
                break

    return factors


def get_primes():
    """Generator that yields prime numbers."""
    num = 2
    while True:
        if is_prime(num): yield num
        num += 1


def get_prime_days(my_date=date.today()):
    """Generator that determines the next prime day after a given point.
    
    The starting point can be passed in as an argument, but defaults to
    the current date of your machine.
    """

    day = my_date.day
    month = my_date.month
    year = my_date.year

    while True:
        if is_day_prime(my_date):
            yield my_date
        try:
            day += 1
            my_date = date(year, month, day)
            continue
        except ValueError:
            try:
                day = 1
                month += 1
                my_date = date(year, month, day)
                continue
            except ValueError:
                try:
                    month = 1
                    year += 1
                    my_date = date(year, month, day)
                    continue
                except ValueError:
                    print('Exceeded year 9999')
                    break


def get_prime_birthdays(year, month, day):
    """Generator that calculates your prime birthdays. 
    
    Birth year, month, and date must be specified as parameters.
    """

    start_year = date.today().year

    while True:
        try:
            birthday = date(start_year, month, day)
            if is_day_prime(birthday):
                yield 'Your {} birthday is a prime year!'.format(start_year - year)
            start_year += 1
        except ValueError:
            print('Cannot exceed year 9999')
            break


if __name__ == '__main__':
    """Usage: python prime_days.py [, numNextPrimeDays]"""
    start = 1 if len(sys.argv) < 2 else int(sys.argv[1])

    for i, prime_day in enumerate(get_prime_days()):
       if i >= start: break
       print(prime_day)

