from datetime import datetime

def time_exec(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(f"Execution time: {datetime.now() - start}")
        return result
    return wrapper