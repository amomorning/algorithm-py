import functools as ft

# reduce
from operator import mul
a = [1, 2, 3, 6, 8]
ft.reduce(mul, a)

def div(a, b):
    return a/b

ft.reduce(div, a)

# custom cmp function
# 1: higher order
# -1: lower order
# 0: same order
def cmp(a, b):
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        return 0

list(sorted(a, key=ft.cmp_to_key(cmp)))
min(a, key=ft.cmp_to_key(cmp))

import time
# use cache
@ft.cache
def factorial(n):
    return n * factorial(n-1) if n else 1


import sys; sys.setrecursionlimit(10**6)
factorial(1200)
factorial(1000) # will use cache

# partial
triple = ft.partial(mul, 3)
triple(12)

list(map(triple, range(10)))


# wraps
# without wraps, the original name and doc string will lost
def deco(func):
    @ft.wraps(func) # try to omit this line
    def wrapper(*args, **kwargs):
        print('Calling decorated function')
        return func(*args, **kwargs)
    return wrapper

@deco
def example():
    """Docs """
    print('Calling example function')

print(example.__name__)
print(example.__doc__)
