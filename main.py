import os
import argparse
import sys
import time

import psutil
import threading
import pandas
import logging
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

def check_etc_usage():
    info = []

    load_memory = psutil.virtual_memory()
    info.append(load_memory[2])

    load_disk = psutil.disk_usage('/')
    info.append(load_disk.percent)

    return info

def parse_arguments():
    parser = argparse.ArgumentParser(description="Enter the time in seconds.")
    parser.add_argument('--time', type=int, default=30)
    return parser.parse_args()

def main(timer):
    logging.info("start to check LPU-B information")
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    GPU_df = pandas.DataFrame(check_GPU_info(), columns=[date], index=["temperature", "usage", "memory usage"])
    cpu_label, cpu_temp = check_CPU_temp()
    CPU_df = pandas.DataFrame(cpu_temp, columns=[date], index=cpu_label)
    usage_df = pandas.DataFrame(check_etc_usage(), columns=[date], index=["memory", "disk"])
    while True:
        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        GPU_df[date] = check_GPU_info()
        cpu_name, cpu_temp = check_CPU_temp()
        CPU_df[date] = cpu_temp
        usage_df[date] = check_etc_usage()

        GPU_df.to_csv("./data/GPU.csv")
        CPU_df.to_csv("./data/CPU_temp.csv")
        usage_df.to_csv("./data/usage_info.csv")
        print(now, "saving")
        logging.info("saved file")
        time.sleep(timer)

if __name__ == '__main__':
    parmeter = parse_arguments()
    logging.info(f"set time is {parmeter.time}")
    main(parmeter.time)
