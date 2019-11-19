import sandbox.main
import functools


class Help:

    def test(self):
        print("test")


def dec(fun):
    @functools.wraps(fun)
    def wrapper(*args):
        print("wrapper")
        ret = fun(*args)
        return ret
    return wrapper


def other(self):
    print("Other")


if __name__ == '__main__':
    h = Help()
    h.test()
    setattr(Help, "test", other)
    h.test()
