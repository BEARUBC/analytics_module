import random 
import time
import threading

def exponential_backoff_decorator(base_delay_in_seconds, logger, max_retries=None):
    """
    A thread-safe retry decorator to enable retrying certain operations with an 
    exponential backoff.
    """
    lock = threading.Lock()
    def decorator(func):
        def wrapper(*args, **kwargs):
            with lock:
                retries = 0
                keep_retrying = False
                if max_retries is None:
                    keep_retrying = True
                while keep_retrying or retries < max_retries:
                    try:
                        result_func = func(*args, **kwargs)
                        return result_func
                    except Exception as e:
                        logger.info(f"Attempt {retries + 1} for {func.__name__} failed: {e}")
                        retries += 1
                        delay = (base_delay_in_seconds * 2 ** retries + random.uniform(0, 1))
                        logger.info(f"Retrying {func.__name__} in {delay:.2f} seconds...")
                        time.sleep(delay)
                raise Exception(f"Max retries reached, {func.__name__} failed.")
        return wrapper
    return decorator