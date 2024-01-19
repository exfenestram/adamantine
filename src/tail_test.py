from tail_recursive import tail_recursive, recurse
from time_exec import time_exec
from pyrsistent import l, plist
from operator import *


@tail_recursive
def factorial(n, acc=l()):
    "calculate a factorial"
    if n == 0:
        return acc
    return recurse(n-1, acc*n)


@tail_recursive
def reduce(f, acc, l):
    if not l:
        return acc
    return recurse(f, l.rest, f(acc, l.first))


@tail_recursive
def generate_list(n, acc=None):
    if n == 0:
        return acc
    return recurse(n-1, acc.cons(n) if acc else l(n))

@tail_recursive
def reverse(ls, acc=None):
    if not ls:
        return acc
    return recurse(ls.rest, acc.cons(ls.first) if acc else l(ls.first))


@tail_recursive
def _map(f, ls, acc=None):
    if not ls:
        return acc
    return recurse(f, ls.rest, acc.cons(f(ls.first)) if acc else l(f(ls.first)))

def map(f, ls):
    return reverse(_map(f, ls))

def mapper(i):
    ls = generate_list(i)
    ls = reverse(ls)
    return ls



# A Tail Recursive function to count down from n to 0
@tail_recursive
def count_down(n):
    if n == 0:
        return 0
    
    return recurse(n-1)

# An iterative function to count down from n to 0
def count_down_iter(n):
    while n > 0:
        n -= 1
    return "Done!"

def dec(a):
    return a-1

def count_down_call(n):
    while n > 0:
        n = dec(n)
    return "Done!"
    
def count_down_range(n):
    for i in range(n, 0, -1):
        pass
    return "Done!"

if __name__ == '__main__':

    #time_exec(count_down)(10000000)
    #time_exec(count_down_call)(10000000)
    #time_exec(count_down_range)(10000000)

    print(time_exec(map)(mapper, plist(range(1, 10))))