# This file is part of Adamantine
# See the LICENSE file for more information
# Copyright 2024, Raymond Richardson

from datetime import datetime

def time_exec(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(f"Execution time: {datetime.now() - start}")
        return result
    return wrapper