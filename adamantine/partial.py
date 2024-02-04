
class _Partial:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*self.args, *args, **self.kwargs, **kwargs)
    

def papply(func, *args, **kwargs):
    return _Partial(func, *args, **kwargs)

