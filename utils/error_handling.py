import logging


# by default returns None if catches an Exception
# also logs the exception
def onerror(*errors, ret=None, warning: str = None, error: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                if error:
                    logging.error(error)
                elif warning:
                    logging.warning(warning)
                return ret
        return wrapper
    return decorator
