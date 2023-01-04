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
        information_list = [GPU_temp.read().rstrip(), GPU_usage.read().rstrip(), GPU_memory_usage.read().rstrip()]
    except:
        return sys.exit("nvidia shell script error! check your nvidia driver")
    return information_list

def check_CPU_temp():
    temp = []
    label = []
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("can't read any temperature")

    if "coretemp" in temps:
        entries = temps["coretemp"]
        for entry in entries:
            label.append(entry.label)
            temp.append(entry.current)

        return label, temp

    else:
        sys.exit("can't get core temperatures")

def check_CPU_usage(time):
    return psutil.cpu_percent(interval=time)

def check_memory_usage():
    mem = psutil.virtual_memory()
    print('memory usage :', mem[2], '%')

def check_disk_usage():
    disk = psutil.disk_usage('/')
    print('disk usage :', disk.percent, '%')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Enter the time in seconds.")
    parser.add_argument('--time', type=int, default=30)
    return parser.parse_args()

def main(time):
    now_day = str(datetime.now().date())
    now_time = str(datetime.now().time())
    GPU_df = pandas.DataFrame(check_GPU_info(), columns=["GPU"], index=["temperature", "usage", "memory usage"])
    print(GPU_df)
    cpu_label, cpu_temp = check_CPU_temp()
    CPU_df = pandas.DataFrame(cpu_temp, columns=["CPU Temperature"], index=cpu_label)
    print(CPU_df)
    return

if __name__ == '__main__':
    parmeter = parse_arguments()
    main(parmeter.time)
