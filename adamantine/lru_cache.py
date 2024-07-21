import pyrsistent as pyr
from threading import Lock


class _cache_node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"({_cache_node.__name__} {self.key} {self.value})"

    def __str__(self):
        return f"({_cache_node.__name__} {self.key} {self.value})"

class _cache_list:
    def __init__(self):
        self.head = None
        self.tail = None
        self.map = pyr.pmap()  # map from key to node

    def append(self, node):
        assert isinstance(node, _cache_node) , f"Expected {_cache_node.__name__} got {type(node)}"
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        # add node to map
        self.map = self.map.set(node.key, node)
        return node

    def unlink(self, node):
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next
        if self.tail == node:
            self.tail = node.prev
        node.next = None
        node.prev = None
        return node

    def move_to_end(self, node):
        self.unlink(node)
        return self.append(node)

    def peek(self):
        node = self.head
        return node
    
    def remove(self, node):
        self.unlink(node) 
        self.map = self.map.remove(node.key)
        return node

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next


# Class LRUCache is an efficient LRU cache implementation. It takes a parameter size which determines the
# capacity of the cache. If the size is None, the cache will have an infinite capacity. 
# The cache is implemented using a persistent dictionary and a persistent queue.

class LRUCache:
    def __init__(self, size=None):
        self.size = size
        self.cache = pyr.pmap()
        self.lru = _cache_list()
        self.lock = Lock()
        if size == None:
            self.put = self.unbound_put
            self.get = self.unbound_get
        else:
            self.put = self.bound_put
            self.get = self.bound_get
            
        self.hits = 0
        self.misses = 0
            
    
    # This method returns the value associated with the key in the cache.
    def bound_get(self, key):
        with self.lock:
            # get node from self.lru.map
            node = self.lru.map.get(key)
            if node is not None:
                value = node.value
                self.lru.move_to_end(node)
                self.hits += 1
                return value
        self.misses += 1
        return None

    def unbound_get(self, key):
        with self.lock:
            value = self.cache.get(key)
            if value is not None:
                self.hits += 1
                return value
            else:
                self.misses += 1
                return None
        
    # This method puts the key-value pair in the cache. If the cache is full, it removes the least recently used
    # key-value pair from the cache.
    def bound_put(self, key, value):
        with self.lock:
            if len(self.cache) >= self.size:
                # Get the oldest node with a pop()
                lru_key_node = self.lru.peek()
                lru_key = lru_key_node.key
                # Remove the oldest key from the cache
                self.cache = self.cache.remove(lru_key)
                # Remove the oldest key from the LRU Index
                self.lru.remove(lru_key_node)
            self.cache = self.cache.set(key, value)
            # Create a node out of lru_key and append it to the LRU Index
            self.lru.append(_cache_node(key, value))
            
            
    def unbound_put(self, key, value):
        with self.lock:
            self.cache = self.cache.set(key, value)
            #self.lru = self.lru.append(_cache_node(key, value))
            
    # This method clears the cache.
    def clear(self):
        with self.lock:
            self.cache = pyr.pmap()
            self.lru = _cache_list()
            self.hits = 0
            self.misses = 0
        

# The function arg_key takes the args and kwargs of a function and returns a key that can be used to identify
# the function call. This key is used to store the result of the function call in the cache.
def arg_key(args, kwargs):
    return (tuple(args), tuple(sorted(kwargs.items())))

# the function lru_cache takes a size parameter which determines the capacity of the cache. It returns a decorator
# that can be used to cache the results of a function call.
def cached(max_size=None):
    cache = LRUCache(max_size)    
    def decorator(func):
        
        def wrapper(*args, **kwargs):
            key = arg_key(args, kwargs)
            value = cache.get(key)
            if value is None:
                value = func(*args, **kwargs)
                cache.put(key, value)
            return value
        wrapper._lru_cache = cache
        return wrapper
    return decorator

def clear_cache(wrapper):
    if hasattr(wrapper, "_lru_cache"):
        lru = wrapper._lru_cache
        if isinstance(lru, LRUCache):
            lru.clear()
    return wrapper

def get_cache(wrapper):
    if hasattr(wrapper, "_lru_cache"):
        lru = wrapper._lru_cache
        if isinstance(lru, LRUCache):
            return lru
    return None

