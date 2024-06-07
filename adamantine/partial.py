from pyrsistent import pvector


class _Partial:
    def __init__(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError("papply must be called with a callable object.")
        
        if hasattr(func, 'func'):
            self.func = func.func
        else:
            self.func = func

        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*self.args, *args, **self.kwargs, **kwargs)
    
    def __repr__(self):
        return f"<Partial {self.func.__name__} {self.args} {self.kwargs}>"
    
    def __str__(self):
        return f"<Partial {self.func.__name__} {self.args} {self.kwargs}>"
    
    
    

def papply(func, *args, **kwargs):
    return _Partial(func, *args, **kwargs)


class Composed:
    def __init__(self, rev, *funcs):
        if rev:
            self.funcs = pvector(funcs.reverse())    
        else:
            self.funcs = pvector(funcs)
        
    def __call__(self, *args, **kwargs):
        res = args
        for func in self.funcs:
            res = func(*res, **kwargs)
        return res
    
    def __repr__(self):
        return f"<Composed {self.funcs}>"
    
    def __str__(self):
        return f"<Composed {self.funcs}>"
    
def compose(*funcs):
    return Composed(True, *funcs)

def compose_left(*funcs):
    return Composed(False, *funcs)