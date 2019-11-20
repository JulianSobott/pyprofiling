"""

"""
from functools import wraps
from attributes import IGNORE, SAVE, STOP

__all__ = ["ignore", "stop", "save"]


def ignore(func):
    """Do not profile this function and all functions that are called inside it recursively."""
    func.__dict__[IGNORE] = True
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def stop(func):
    """Stops the program and saves the profile to the file when this function is called"""
    func.__dict__[STOP] = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def save(func):
    """Saves the profiler and stops it. The program continues as normal"""
    func.__dict__[SAVE] = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
