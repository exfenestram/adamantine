
# apply call a function with arguments. Trivial in Python, but usefule as a function 

def apply(func, *args, **kwargs):
    return func(*args, **kwargs)

# Given a list of callables, return the list of results of calling each callable with the same arguments
def apply_list(list, *args, **kwargs):
    return [apply(func, *args, **kwargs) for func in list]
