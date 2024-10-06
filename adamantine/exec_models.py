# This file is part of Adamantine
# See the LICENSE file for more information
# Copyright 2024, Raymond Richardson




# This module provides a more complex map function and reduce function
# map is implemented as a generator


# This function is a generator that takes a function and a list of arguments
# and returns the result of applying the function to each of the arguments
# in the list.  If the function takes more than one argument, the arguments
# are taken from the lists in parallel.  If the lists are of different lengths,
# the result will be the same length as the shortest list.

from collections import deque
from collections.abc import Mapping, Sequence, Set
from pyrsistent import *
from operator import *


def is_empty(container):
    return not container


def map_iter(f, *args):
    if not args:
        return
    if len(args) == 1:
        for item in args[0]:
            yield f(item)
    else:
        for item in zip(*args):
            yield f(*item)

def map(f, *args):
    return pvector(map_iter(f, *args))


def cmap_iter(f, *args):
    if not args:
        return
    if len(args) == 1:
        for item in args[0]:
            try:
                yield f(item)
            except Exception as e:
                pass
    else:
        for item in zip(*args):
            try:
                yield f(*item)
            except Exception as e:
                pass

def cmap(f, *args):
    return pvector(cmap_iter(f, *args))

def emap_iter(f, *args):
    if not args:
        return
    if len(args) == 1:
        for item in args[0]:
            try:
                yield f(item)
            except Exception as e:
                yield e
    else:
        for item in zip(*args):
            try:
                yield f(*item)
            except Exception as e:
                yield e

def emap(f, *args):
    return pvector(emap_iter(f, *args))


# foldl computes its result by applying the first elements of a sequence of iterators
# to the function, then applying the second elements of the iterators to the function,
# and so on until the iterators are exhausted.  If the iterators are of different lengths,
# the result will be the same length as the shortest iterator.  If the iterators are empty,
# reduce will raise StopIteration unless initializer is set - if so, it returns initionalizer.
#  If an initializer is provided, it will be used as the
# first argument to the function.  If no initializer is provided, the tuple of the first elements
# of the iterators will be used as the first argument to the function.


def foldl(f, initializer, *args):
    '''Multi Argument List Reduce Function'''
    for item in zip(*args):
        initializer = f(initializer, *item)

    return initializer

    
def groupby(data, key=lambda x: x, value=lambda x: x):
    res = m()
    for item in data:
        k = key(item)
        v = value(item)
        if k not in res:
            new = l(v)
        else:
            new = res[k].cons(v)
        res = res.set(k, new)
    return res

def groupby_set(data, key=lambda x: x):
    res = m()
    for item in data:
        k = key(item)
        if k not in res:
            new = s(item)
        else:
            new = res[k].add(item)
        res = res.set(k, new)
    return res

def group_count(data, key=lambda x: x):
    res = m()
    for item in data:
        k = key(item)
        if k not in res:
            new = 1
        else:
            new = res[k] + 1
        res = res.set(k, new)
    return res


def merge(it1, it2, key=lambda x: x, reverse=False):
    it1 = iter(it1)
    it2 = iter(it2)

    if reverse:
        op = ge
    else:
        op = le
    try:
        item1 = next(it1)
    except StopIteration:
        return it2
    try:
        item2 = next(it2)
    except StopIteration:
        return it1
    while True:
        if op(key(item1),key(item2)):
            yield item1
            try:
                item1 = next(it1)
            except StopIteration:
                yield item2
                yield from it2
                return
        else:
            yield item2
            try:
                item2 = next(it2)
            except StopIteration:
                yield item1
                yield from it1
                return
            


def juxtapose_iter(funcit, *args, **kwargs):
    ''' Call multiple functions with the same arguments'''
    for f in funcit:
        yield f(*args, **kwargs)

def juxtapose(funcit, *args, **kwargs):
    ''' Call multiple functions with the same arguments'''
    return pvector(juxtapose_iter(funcit, *args, **kwargs))


def pairwise_iter(comp_func, cmp, argslist):
    ''' Compare pairs of arguments using a comparison function'''
    return (comp_func(cmp, arg) for arg in argslist)

def pairwise_chain_iter(comp_func, argslist):
    ''' Compare each element of args list with the next item'''
    return (comp_func(argslist[i], argslist[i+1]) for i in range(len(argslist)-1))
 
def pairwise(comp_func, cmp, argslist):
    ''' Compare pairs of arguments using a comparison function'''
    return pvector(pairwise_iter(comp_func, cmp, argslist))    

def pairwise_chain(comp_func, argslist):
    ''' Compare each element of args list with the next item'''
    return pvector(pairwise_chain_iter(comp_func, argslist))


# Walk takes a collection and applies a function to each element of the collection.
# It returns a new collection of the same type as the input collection.

def walk(func, collection):
    
    if isinstance(collection, deque):
        return pdeque(func(item) for item in collection)
    elif isinstance(collection, PDeque):
        return pdeque(func(item) for item in collection)
    elif isinstance(collection, Mapping):
        return pmap(func(key, value) for key, value in collection.items())
    elif isinstance(collection, Set):
        return pset(func(item) for item in collection)
    elif isinstance(collection, PList):
        return plist(func(item) for item in collection)
    elif isinstance(collection, PBag):
        return pbag(func(item) for item in collection)
    elif isinstance(collection, tuple):
        return tuple(func(item) for item in collection)
    elif isinstance(collection, str):
        chars = pvector(func(item) for item in collection)
        return ''.join(chars)
    elif isinstance(collection, Sequence):
        return pvector(func(item) for item in collection)
    else:
        raise TypeError(f"Unsupported collection type: {type(collection)}")
