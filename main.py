import os
import argparse
import sys
import psutil
import threading
import pandas
from datetime import datetime

def check_GPU_info():
    try:
        GPU_temp = os.popen("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader")
        GPU_usage = os.popen("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader")
        GPU_memory_usage = os.popen("nvidia-smi --query-gpu=utilization.memory --format=csv,noheader")
        information_list = {
            "temperature": GPU_temp.read().rstrip(),
            "usage": GPU_usage.read().rstrip(),
            "memory_usage": GPU_memory_usage.read().rstrip()
        }

    except:
        return sys.exit("nvidia shell script error! check your nvidia driver")
    return information_list

def check_CPU_temp():
    CPU_information = {}
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("can't read any temperature")

    if "coretemp" in temps:
        entries = temps["coretemp"]
        CPU_information["temperature"] = {}
        for entry in entries:
            CPU_information["temperature"][entry.label] = entry.current

        return CPU_information

    else:
        sys.exit("can't get core temperatures")

def check_CPU_usage(time):
    return psutil.cpu_percent(interval=time)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Enter the time in seconds.")
    parser.add_argument('--time', type=int, default=30)
    return parser.parse_args()

def main(time):
    print(datetime.now())
    # CPU usage
    # t1= threading.Thread(target=check_CPU_usage, args=(time,))
    # t1.start()
    print(check_CPU_temp())
    print(check_GPU_info())
    return

if __name__ == '__main__':
    parmeter = parse_arguments()
    main(parmeter.time)
