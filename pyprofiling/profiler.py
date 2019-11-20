import threading
from datetime import datetime
import json
import os

separator = ""


class Profiler:

    instance: "Profiler" = None

    def __init__(self, program_name, profile_name):
        self.program_name = program_name
        self.profile_name = profile_name
        Profiler.instance = self

    def __enter__(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        # TODO: set proper file path: Maybe create new folder in users project and save all files in it
        self.file_path = os.path.join(project_dir, self.program_name + "_" + self.profile_name + ".json")
        self.file = open(self.file_path, "w")
        self.file.write('{"otherData": {}, "traceEvents":[')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.write("]}")
        print("Successfully saved profile in: " + Profiler.instance.file_path)
        self.file.close()

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

    def __enter__(self):
        self.start_time = datetime.now().microsecond

    def run(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now().microsecond
        Profiler.write_method(self.function_name, self.start_time, self.end_time, self.thread_name)
