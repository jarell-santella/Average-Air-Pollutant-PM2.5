import os
from argparse import ArgumentTypeError

def positive_int(value):
    # If value is not a positive integer, raise ValueError
    value = int(value)
    if value < 1:
        raise ValueError
    return value

def reasonable_positive_int(value):
    # If value is not a positive integer less than or equal to min(32, os.cpu_count() + 4), raise ValueError
    # Used to avoid performance issues
    # See default max_threads https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
    value = positive_int(value)
    if positive_int(value) > min(32, os.cpu_count() + 4):
        raise ArgumentTypeError('Too high for your CPU count. Try a lower a rate.')
    return value