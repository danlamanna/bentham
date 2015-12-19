from __future__ import absolute_import
from bentham.trackers import app


def recursive_fib(n):
    if n < 2:
        return n
    return recursive_fib(n - 2) + recursive_fib(n - 1)


@app.task
def async_fib(n):
    return recursive_fib(n)
