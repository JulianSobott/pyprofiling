from typing import TextIO
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
