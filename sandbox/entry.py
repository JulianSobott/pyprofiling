from pyprofiling.base import profile
import sandbox


def start_entry():
    profile(sandbox.main.start_sandbox, globals(), "sandbox", "first_try")


if __name__ == '__main__':
    start_entry()
