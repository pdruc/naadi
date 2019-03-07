import glob
import os
import subprocess
import time

import pandas as pd


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        reference_time = time.monotonic()
        func(*args, **kwargs)
        t = time.monotonic() - reference_time
        wrapper.te = [int(t // 60), int(t % 60)]

    return wrapper


def measure_time_elapsed(reference_time):
    t = time.monotonic() - reference_time
    return [int(t // 60), int(t % 60)]


def count_process_instances(process_name):
    return subprocess.Popen(['pgrep', '-c', process_name], stdout=subprocess.PIPE).communicate()[0]


def execute_system_command_and_wait(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]


def execute_system_command_and_continue(command):
    subprocess.Popen(command, stdout=subprocess.DEVNULL)
    return None


def get_latest_file(directory):
    list_of_files = glob.glob(directory + '*')
    return max(list_of_files, key=os.path.getctime)


def get_directory_content(directory):
    return os.listdir(directory)


def build_attributes_df(obj):
    return pd.DataFrame({'variable': [str(k) for k in obj.__dict__.keys()],
                         'type': [str(type(v)) for v in list(obj.__dict__.values())],
                         'origination': [str(type(obj))] * len(obj.__dict__)})


def hex2rgb(hex, opacity=1):
    return 'rgba' + str(tuple([int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:], 16), opacity]))
