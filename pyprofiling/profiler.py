import threading
import time
import json
import os

from Logging import logger
from attributes import STOP_AFTER, STOP_BEFORE, STOP_IN_SECONDS, SAVE, IGNORE

separator = ""


class Profiler:

    instance: "Profiler" = None

    def __init__(self, program_name, profile_name):
        self.program_name = program_name
        self.profile_name = profile_name
        self._saved = False
        Profiler.instance = self

    def __enter__(self):
        project_dir = os.getcwd()
        profile_folder = os.path.join(project_dir, "profiles")
        os.makedirs(profile_folder)
        self.file_path = os.path.join(profile_folder, self.program_name + "_" + self.profile_name + ".json")
        self.file = open(self.file_path, "w")
        self.file.write('{"otherData": {"version": "'+self.program_name + self.profile_name+'"}, "traceEvents":[')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    @staticmethod
    def save():
        if not Profiler.instance._saved:
            Profiler.instance.file.write(']}')
            print("Successfully saved profile in: " + Profiler.instance.file_path)
            Profiler.instance.file.close()
            Profiler.instance._saved = True

    @staticmethod
    def write_method(name, start_time, end_time, thread_id):
        global separator
        dur_microseconds = (end_time - start_time)
        data = {"cat": "function",
                "dur": dur_microseconds,
                "name": name,
                "ph": "X",
                "pid": "0",
                "tid": thread_id,
                "ts": start_time}
        Profiler.instance.file.write(separator + json.dumps(data))
        separator = ", "


class FunctionRunner:

    def __init__(self, func, is_descriptor):
        self.func = func.__func__ if is_descriptor else func
        self.is_descriptor = is_descriptor
        self.function_name = func.__func__.__name__ if is_descriptor else func.__name__
        self.thread_name = threading.current_thread().name
        self.stop_after = False
        self.stop_before = False
        self.ignore = False
        self.save = False

    def __enter__(self):
        self.ignore = self.is_ignore()
        self.stop_after = self.is_in_dict(STOP_AFTER)
        self.stop_before = self.is_in_dict(STOP_BEFORE)
        self.save = self.is_in_dict(SAVE)
        self.start_time_ns = time.time_ns()
        if self.is_in_dict(STOP_IN_SECONDS):
            self.handle_stop_in_seconds()
        if self.stop_before:
            stop_application()
        return self

    def run(self, *args, **kwargs):
        if not global_data.stop_executing_functions:
            return self.func(*args, **kwargs)
        else:
            self.ignore = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time_ns = time.time_ns()
        if not self.ignore and global_data.profile_is_on:
            Profiler.write_method(self.function_name, self.start_time_ns/1000, self.end_time_ns/1000, self.thread_name)
        if self.stop_after:
            stop_application()

        if self.save:
            Profiler.save()
            global_data.stop_profile()

    def is_ignore(self):
        if self.is_in_dict(IGNORE):
            return True
        if self.thread_name in global_data.ignores_in_thread:
            return True
        return False

    def is_in_dict(self, name: str):
        if name in self.func.__dict__:
            return True
        return False

    def handle_stop_in_seconds(self):
        import time
        seconds = self.func.__dict__[STOP_IN_SECONDS]

        def t():
            time.sleep(seconds)
            global_data.stop_executing()
            stop_application()
        threading.Thread(target=t).start()


class GlobalData:

    def __init__(self):
        self.ignores_in_thread = set()
        self.profile_is_on = True
        self.stop_executing_functions = False

    def stop_profile(self):
        self.profile_is_on = False

    def stop_executing(self):
        self.stop_executing_functions = True


global_data = GlobalData()


def stop_application():
    for thread in threading.enumerate():
        try:
            thread.stop()
        except Exception as e:
            logger.debug(str(e) + "  " + thread.name)
