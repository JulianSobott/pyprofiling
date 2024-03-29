import functools
import threading
import time
from pyprofiling import *


def fun1():
    time.sleep(1)


def fun2():
    for i in range(1, 100000):
        x = i / i
        x += FirstClass.math.sqrt(i)


def fun3(s):
    time.sleep(s)


def start_sandbox():
    # fun2(10, x=10)
    fun1()
    fun3(1)
    f = FirstClass()
    t1 = threading.Thread(target=f.do_something, name="Thread1InMain")
    t2 = threading.Thread(target=fun2, name="Thread2InMain")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    fun1()
    fun2()
    FirstClass.stats()


def dec(f):
    @functools.wraps(f)
    def wrapper(*args):
        return f(*args)
    return wrapper


def class_dec(f):
    @functools.wraps(f)
    def wrapper(*args):
        return f.__func__(*args)

    return wrapper


class FirstClass:
    import math

    def do_something(self):
        for i in range(1, 10000):
            x = i / i
            x += FirstClass.math.sqrt(i)
        for i in range(3):
            fun2()
            time.sleep(0.001)
        return self

    @classmethod
    def stats(cls):
        print("stats")

    @staticmethod
    def stats2(self):
        return 10

#
# setattr(FirstClass, "stats", dec(FirstClass.__dict__["stats"]))


if __name__ == '__main__':
    start_sandbox()
