import functools
from time import perf_counter

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took: {perf_counter() - t0:.2f}s")
        return result
    return wrapper

