import threading
from datetime import datetime
import json
import os

from attributes import STOP_AFTER, STOP_BEFORE, SAVE, IGNORE

separator = ""


class Profiler:

    instance: "Profiler" = None

    def __init__(self, program_name, profile_name):
        self.program_name = program_name
        self.profile_name = profile_name
        self._saved = False
        Profiler.instance = self

    def __enter__(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        # TODO: set proper file path: Maybe create new folder in users project and save all files in it
        self.file_path = os.path.join(project_dir, self.program_name + "_" + self.profile_name + ".json")
        self.file = open(self.file_path, "w")
        self.file.write('{"otherData": {}, "traceEvents":[')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    @staticmethod
    def save():
        if not Profiler.instance._saved:
            Profiler.instance.file.write("]}")
            print("Successfully saved profile in: " + Profiler.instance.file_path)
            Profiler.instance.file.close()
            Profiler.instance._saved = True

    @staticmethod
    def write_method(name, start_time, end_time, thread_id):
        global separator
        data = {"cat": "function",
                "dur": end_time - start_time,
                "name": name,
                "ph": "X",
                "pid": "0",
                "tid": thread_id,
                "ts": start_time}
        Profiler.instance.file.write(separator + json.dumps(data))
        separator = ", "


class FunctionRunner:

    # TODO: Handle modifiers: ignore, stop, save, ...

    def __init__(self, func, is_descriptor):
        self.func = func
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
        self.start_time = datetime.now().microsecond
        if self.stop_before:
            exit(0)
        return self

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now().microsecond
        if not self.ignore and global_data.profile_is_on:
            Profiler.write_method(self.function_name, self.start_time, self.end_time, self.thread_name)
        if self.stop_after:
            exit(0)

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


class GlobalData:

    def __init__(self):
        self.ignores_in_thread = set()
        self.profile_is_on = True

    def stop_profile(self):
        self.profile_is_on = False


global_data = GlobalData()
