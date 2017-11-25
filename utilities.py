import math


# Below are the helper functions for ray tracing
# The function returns 1 for positive number and -1 for negative number
# For 0 it depends on platform.
def sign(value):
    return int(math.copysign(1, value))


# Returns the integer part of the number
def integer_part(x):
    """Floors x."""
    return math.floor(x)


# Returns the rounded integer number
def integer_round(x):
    """Rounds x to the nearest integer."""
    return integer_part(x + 0.5)


# Returns the fractional part of the number
def fractional_part(x):
    """Returns the fractional part of x."""
    return x - math.floor(x)


# Return 1 - fractional part of the number
def rfractional_part(x):
    """Returns the 1 minus the fractional part of x."""
    return 1 - fractional_part(x)