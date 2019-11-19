from pyprofiling.base import profile
import main


def start_entry():
    profile(main.start_sandbox, globals())


if __name__ == '__main__':
    start_entry()
