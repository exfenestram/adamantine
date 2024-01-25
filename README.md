# adamantine
Tools for Immutable/Functional programming in Idiomatic Python

Adamantine contains some useful functional programming modules

tail_recursion implements a somewhat efficient tail recursion optimization
To Use it, import the tail_recursion module and use the @tail_recursion annotation 
on the function to be optimized. When making the recursive call, instead of calling the 
function call recurse(*args, **kwargs)
This optimization uses a continuation based methodology rather than using exception handling
and is about 4-5 x slower than a simple for loop which calls a function 

exec_models implements map and reduce with multiple input lists. The element of each list is 
used as a separate parameter to the map or reduce function. i.e.


