import functools
import threading


def fun1(x):
    return 10 + x


def fun2():
    for i in range(1, 100000):
        x = i / i
        x += FirstClass.math.sqrt(i)


def start_sandbox():
    # x = 10
    # fun1(x)
    # fun2(10, x=10)
    f = FirstClass()
    t1 = threading.Thread(target=f.do_something)
    t2 = threading.Thread(target=fun2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # f.stats2()
    #FirstClass.stats()


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
