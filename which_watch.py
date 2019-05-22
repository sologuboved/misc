import time


def which_watch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print()
        print(func.__name__, 'took', time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))
        print()
        return result

    return wrapper
