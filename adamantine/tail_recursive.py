# This file is part of Adamantine
# See the LICENSE file for more information
# Copyright 2024, Raymond Richardson

from pyrsistent import plist, l

# This Module provides simple tail recursion for Python.
# It is implemented using a decorator and a continuation
# class.  The decorator replaces the decorated function
# with a continuation class if the function is called
# recursively.  The continuation class is resolved by
# the decorator and the recursion continues.  This
# allows for tail recursion to occur without the
# possibility of a stack overflow.

# This module is not thread safe. If multiple threads were to invoke tail
# recursive functions, the continuations would be shared between the threads
# and the results would be unpredictable.  This is not a problem for the
# intended use of this module, which is to allow for tail recursion in
# Python.  It is not intended to be used in a multi-threaded environment.






# This class is a simple continuation class that allows for tail recursion
# in Python.  It is used by the tail_recursive decorator below.

class _Continuation:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def set_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def _resolve_(self):
        return self.fn(*self.args, **self.kwargs)

_allocated = l()

_conts = [_Continuation(), _Continuation()]
_index = 0


class ContinuationPair():
    def __init__(self):
        self._conts = [_Continuation(), _Continuation()]
        self._index = 0
    
    def get_continuation(self):
        res = self._conts[self._index]
        self._index ^= 1
        return res


def get_continuation():
    global _allocated
    return _allocated.first.get_continuation()

def enter_function():
    global _allocated
    _allocated = _allocated.cons(ContinuationPair())

def exit_function():
    global _allocated
    _allocated = _allocated.rest


# This is the function to be used instead of a recursive call 
# in a tail recursive function.  It takes the same arguments 
# as the function it is used in and returns a _Recurse object
# that can be used to continue the recursion.  The _Recurse
# object is resolved by the tail_recursive decorator below.
    
def recurse(*args, **kwargs):
    global _top
    recur = get_continuation()
    recur.args = args
    recur.kwargs = kwargs
    return recur


# This is the decorator that allows tail recursion to occur.
# It works by replacing the decorated function with a
# _Recurse object if it is called recursively.  It then
# continues to call the function and returns the result        
def tail_recursive(f):
    
    def decorated(*args, **kwargs):
        enter_function()
        try:
            result = f(*args, **kwargs)
            while isinstance(result, _Continuation):
                result = f(*result.args, **result.kwargs)
            return result
        except:
            raise
        finally:
            exit_function()

    return decorated
