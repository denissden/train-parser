import logging
import random


def log_process(func):
    def wrapper(*args, **kwargs):
        call_id = id(func)
        logging.info(f'call {func.__qualname__} with id {call_id}')
        ret = func(*args, **kwargs)
        logging.info(f'end {func.__qualname__} with id {call_id}')
        return ret
    return wrapper
