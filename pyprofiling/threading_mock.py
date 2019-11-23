import threading


def stop(self):
    raise threading.ThreadError("Stopping thread")


threading.Thread.stop = stop
