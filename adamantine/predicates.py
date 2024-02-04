from pyrsistent import v, pvector


def include(pred, iterator):
    for el in iterator:
        if pred(el):
            yield el

def exclude(pred, iterator):
    for el in iterator:
        if not pred(el):
            yield el


def split(pred, iterator):
    a = v()
    b = v()
    for el in iterator:
        if pred(el):
            a = a.append(el)
        else:
            b = b.append(el)
    return a, b