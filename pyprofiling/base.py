from types import ModuleType
from functools import wraps
from datetime import datetime
import threading

from .Logging import logger
from .profiler import Profiler, FunctionRunner
from .attributes import PROFILING_ADDED, STOP_AFTER, STOP_BEFORE, SAVE, IGNORE

# TODO: Add docs to functions
# TODO: Maybe make possible to use via console call: profile sandbox.py ...
# TODO: Maybe add more options to ignore certain functions, pause profiler, auto save after X seconds, ...

ignores_in_thread = set()


def gen_wrapper(func, is_descriptor=False, *args, **kwargs):
    global ignores_in_thread
    """

    :param func: a function
    :param is_descriptor: True when wraps a function that is wrapped by a classmethod or staticmethod
    :param args:
    :param kwargs:
    :return:
    """
    # with FunctionRunner(func, is_descriptor) as f:
    #     f.run(*args, **kwargs)
    thread_name = threading.current_thread().name
    function_name = func.__func__.__name__ if is_descriptor else func.__name__
    # TODO: Handle errors -> show stacktrace of original function call
    if IGNORE in func.__dict__.keys():
        ignores_in_thread.add(thread_name)
    if STOP_BEFORE in func.__dict__.keys():
        exit(0)
    start = datetime.now().microsecond
    if is_descriptor:
        ret = func.__func__(*args, **kwargs)
    else:
        ret = func(*args, **kwargs)
    end = datetime.now().microsecond
    if thread_name not in ignores_in_thread:
        Profiler.write_method(function_name, start, end, thread_name)
    if IGNORE in func.__dict__.keys():
        ignores_in_thread.remove(thread_name)
    if STOP_AFTER in func.__dict__.keys():
        exit(1)
    return ret


def profile_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return gen_wrapper(func, False, *args, **kwargs)
    return wrapper


def profile_descriptor(func, cls):
    """descriptors are @staticmethod or @classmethod."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if type(func) == classmethod:
            return gen_wrapper(func, True, cls, *args, **kwargs)
        else:
            return gen_wrapper(func, True, *args, **kwargs)
    return wrapper


def add_decorators(glob: dict, program_name="", is_class=False, class_name="", class_item=None):
    deb_functions_added = []
    for name, item in glob.items():
        x = hasattr(item, "__dict__")
        if callable(item) or hasattr(item, "__func__"):
            if is_class or program_name in item.__module__ or "__main__" in item.__module__:
                if PROFILING_ADDED not in item.__dict__:
                    if isinstance(item, type):
                        add_class(name, item, program_name)
                    else:
                        if is_class:
                            if type(item) in [classmethod, staticmethod]:
                                add_classmethod(name, item, class_item, deb_functions_added)
                            else:
                                add_method(name, item, class_item, deb_functions_added)
                        else:
                            add_function(name, item, glob, deb_functions_added)
                else:
                    pass    # has already decorator
        elif isinstance(item, ModuleType):
            if (hasattr(item, "__path__") and program_name in item.__path__[0]) or program_name in item.__name__:
                if PROFILING_ADDED not in item.__dict__:
                    add_module(item, program_name)
                else:
                    pass    # has already decorators
    if is_class:
        logger.info(f"Added all profile decorators in class:  "
                    f"{class_name.rjust(20, ' ')}: {str(deb_functions_added).ljust(50, ' ')}")
    else:
        logger.info(f"Added all profile decorators in module: "
                    f"{glob['__name__'].rjust(20, ' ')}: {str(deb_functions_added).ljust(50, ' ')}")


def add_function(name, item, glob, deb_functions_added):
    deb_functions_added.append(name)
    item.__dict__[PROFILING_ADDED] = True
    glob[name] = profile_function(item)


def add_method(name, method, class_item, deb_functions_added):
    deb_functions_added.append(name)
    method.__dict__[PROFILING_ADDED] = True
    setattr(class_item, name, profile_function(method))


def add_classmethod(name, method, class_item, deb_functions_added):
    deb_functions_added.append(name)
    method.__dict__[PROFILING_ADDED] = True
    setattr(class_item, name, profile_descriptor(method, class_item))


def add_module(item, program_name):
    item.__dict__[PROFILING_ADDED] = True
    add_decorators(item.__dict__, program_name)


def add_class(class_name, class_item, program_name):
    add_decorators(class_item.__dict__, program_name, is_class=True, class_name=class_name, class_item=class_item)


def profile(func: callable, globals_dict: dict, program_name: str = "", profile_name: str = "profiling_results", *args,
            **kwargs):
    with Profiler(program_name, profile_name):
        if not program_name:
            program_name = func.__module__.split(".")[0]
        add_decorators(globals_dict, program_name)
        profile_function(func)(*args, **kwargs)
