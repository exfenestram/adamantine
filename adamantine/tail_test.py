from tail_recursive import tail_recursive, recurse, recurse_with_fn
from time_exec import time_exec
from pyrsistent import l, plist
from operator import *
from exec_models import *


@tail_recursive
def factorial(n, acc=l()):
    "calculate a factorial"
    if n == 0:
        return acc
    return recurse(n-1, acc*n)


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




def mapper(i, j, k):
    ls = generate_list(i + j - k)
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

def reductor(acc, i, j, k):
    a1 = acc[0] + i
    a2 = acc[1] + j
    a3 = acc[2] + k
    return (a1, a2, a3)

class NotDefined(Exception):
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return "NotDefined " + repr(self.obj)
    
def even(i):
    if i % 2 == 0:
        return i
    else:
        raise NotDefined(i)

def odd(i):
    if i % 2 == 1:
        return i
    else:
        raise NotDefined(i)

@tail_recursive
def mappy(ls):
    if not ls:
        return True
    return recurse_with_fn(each, ls.rest)

@tail_recursive
def each(ls):
    if not ls:
        return True
    print(ls.first)
    return recurse_with_fn(mappy, ls.rest)

        

if __name__ == '__main__':

    time_exec(count_down)(10000000)
    time_exec(count_down_call)(10000000)
    #time_exec(count_down_range)(10000000)

    #print(time_exec(reduce)(reductor, range(1, 100000), range(999999, 0, -1), range(1, 100000  )))

    #print(plist(emap(even, range(1, 10))))
    each(l(1, 2, 3, 4, 5))