import time
import gc


def time_functions(function):
    """
    Compute the time elapsed
    Returns a float
    :param function: some function
    """
    gc.disable()
    start = time.time()
    function()
    stop = time.time()
    gc.enable()
    elapsed = stop - start
    return elapsed
