"""

"""
from functools import wraps
from attributes import IGNORE, SAVE, STOP_AFTER, STOP_BEFORE, STOP_IN_SECONDS

__all__ = ["ignore", "stop_after", "stop_before", "stop_in_seconds", "save"]


def ignore(func):
    """Do not profile this function and all functions that are called inside it recursively."""
    func.__dict__[IGNORE] = True
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def stop_after(func):
    """Stops the program and saves the profile to the file after this function finished executing"""
    func.__dict__[STOP_AFTER] = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def stop_before(func):
    """Stops the program and saves the profile to the file when this function is called"""
    func.__dict__[STOP_BEFORE] = True

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


def stop_in_seconds(seconds):
    def outer_wrapper(func):
        func.__dict__[STOP_IN_SECONDS] = seconds

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return outer_wrapper
