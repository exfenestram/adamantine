from pyrsistent import v, pvector, pdeque


def include(pred, iterator):
    for el in iterator:
        if pred(el):
            yield el

def exclude(pred, iterator):
    for el in iterator:
        if not pred(el):
            yield el


def split(pred, iterator):
    q1 = v()
    q2 = v()
    
    for el in iterator:
        if pred(el):
            q1 = q1.append(el)
        else:
            q2 = q2.append(el)
    
    return iter(q1), iter(q2)
    

def complement(pred):
    def _complement(*args, **kwargs):
        return not pred(*args, **kwargs)
    return _complement


def all_of(predicates):
    def _all_of(*args, **kwargs):
        for pred in predicates:
            if not pred(*args, **kwargs):
                return False
        return True
    return _all_of

def some_of(predicates):
    def _some_of(*args, **kwargs):
        for pred in predicates:
            if pred(*args, **kwargs):
                return True
        return False
    return _some_of


