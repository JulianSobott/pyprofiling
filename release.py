"""
Requirements:

    - Set password and username in keyring see: https://pypi.org/project/twine/ and https://pypi.org/project/keyring/

usage: release.py [-h] [-v VERSION] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        Version of the program
  -t, --test            Release only on `test.pypi.org`

"""
import os
import subprocess
import shutil
import sys

import setup
import re
import argparse


def get_args() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--version", required=False, help="Version of the program")
    ap.add_argument("-t", "--test", required=False, action='store_true', help="Release only on `test.pypi.org`")
    ap.add_argument("-l", "--local", required=False, action="store_true", help="Create only local packages. Not "
                                                                               "publishing.")
    sys_args = vars(ap.parse_args())

    test = sys_args["test"]
    if sys_args["version"]:
        version = sys_args["version"]
    else:
        try:
            file = os.listdir("dist")[0]
            m = re.match(r".*?([0-9]*)\.([0-9]*)\.([0-9]*).*", os.listdir("dist")[0]).regs
            current_version = file[m[1][0]:m[1][1]], file[m[2][0]:m[2][1]], file[m[3][0]:m[3][1]]
            version = list(current_version)
            version[2] = str(int(version[2]) + 1)
            version = ".".join(version)
        except IndexError:
            version = None
        except FileNotFoundError:
            version = None
    name = os.path.split(os.getcwd())[1]
    return {"version": version, "test": test, "name": name, "local": sys_args["local"]}


def release():
    args = get_args()
    shutil.rmtree("dist/", ignore_errors=True)
    subprocess.run("python -m pip install --upgrade setuptools wheel".split(" "))
    sys.argv = ["setup.py", "sdist", "bdist_wheel"]
    if args["version"]:
        setup.main(args["version"])
    else:
        setup.main()

    if not args["local"]:
        subprocess.run("python -m pip install --upgrade twine".split(" "))
        if args["test"]:
            subprocess.run("twine upload --repository-url https://test.pypi.org/legacy/ dist/*".split(" "))
            print(f"Project published on: https://test.pypi.org/project/{args['name']}/")
        else:
            subprocess.run("twine upload dist/*".split(" "))
            print(f"Project published on: https://pypi.org/project/{args['name']}/")


if __name__ == '__main__':
    release()
