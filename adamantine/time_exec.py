# This file is part of Adamantine
# See the LICENSE file for more information
# Copyright 2024, Raymond Richardson

from datetime import datetime



def time_func(func, *args, **kwargs):
    start = datetime.now()
    result = func(*args, **kwargs)
    print(f"Execution time: {datetime.now() - start}")
    return result

def time_exec(func):
    def wrapper(*args, **kwargs):
        return time_func(func, *args, **kwargs)
    return wrapper