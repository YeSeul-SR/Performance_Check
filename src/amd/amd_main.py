import os
import argparse
import sys
import time
import psutil
import pandas
from datetime import datetime


def check_GPU_info():
    try:
        GPU_temp = os.popen(
            "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader"
        )
        GPU_usage = os.popen(
            "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader"
        )
        GPU_memory_usage = os.popen(
            "nvidia-smi --query-gpu=utilization.memory --format=csv,noheader"
        )
        information_list = [
            GPU_temp.read().rstrip(),
            GPU_usage.read().rstrip(),
            GPU_memory_usage.read().rstrip(),
        ]
    except:
        return sys.exit("nvidia shell script error! check your nvidia driver")
    return information_list


def check_CPU_info():
    usage = psutil.cpu_percent(interval=None)
    temp = [usage]
    label = ["CPU usage"]
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("can't read any temperature")

    if "coretemp" in temps:
        entries = temps["coretemp"]
        for entry in entries:
            label.append(entry.label + "-temperature")
            temp.append(entry.current)

        return label, temp

    else:
        sys.exit("can't get core temperatures")


def check_etc_usage():
    info = []

    load_memory = psutil.virtual_memory()
    info.append(load_memory[2])

    load_disk = psutil.disk_usage("/")
    info.append(load_disk.percent)

    return info


def check_network():
    label = []
    status = []
    stats = psutil.net_if_stats()
    error_info = psutil.net_io_counters(pernic=True)
    for nic, addrs in psutil.net_if_addrs().items():
        if nic in stats:
            if stats[nic].isup:
                label.append(nic)
                status.append(stats[nic].isup)
                if nic in error_info:
                    label.append(nic + "-errin")
                    status.append(error_info[nic].errin)
                    label.append(nic + "-errout")
                    status.append(error_info[nic].errout)
                    label.append(nic + "-dropin")
                    status.append(error_info[nic].dropin)
                    label.append(nic + "-dropout")
                    status.append(error_info[nic].dropout)
    return label, status


def get_data():
    timestamp = datetime.now()
    now = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    column = []
    data = []

    cpu_label, cpu_info = check_CPU_info()
    for label in cpu_label:
        column.append(label)
    for info in cpu_info:
        data.append(info)

    GPU_info = check_GPU_info()
    column.append("GPU temperature")
    column.append("GPU usage")
    column.append("GPU memory usage")
    for info in GPU_info:
        data.append(info)

    usage_info = check_etc_usage()
    column.append("Memory usage")
    column.append("Disk Usage")
    for info in usage_info:
        data.append(info)

    net_label, net_status = check_network()
    for label in net_label:
        column.append(label)
    for status in net_status:
        data.append(status)

    return now, data, column


def save_file(df):
    now, data, column = get_data()
    df.loc[now] = data
    df.to_csv("../../data/computer_information.csv")
    print(f"{now}, saved to file")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Enter the time in seconds.")
    parser.add_argument("--time", type=int, default=30)
    return parser.parse_args()


def main(timer):
    now, data, column = get_data()

    df = pandas.DataFrame(data=[data], index=[now], columns=column)

    df.to_csv("../../data/computer_information.csv")
    print(f"{now}, start saved to file")
    time.sleep(timer)
    while True:
        save_file(df)
        time.sleep(timer)


if __name__ == "__main__":
    parmeter = parse_arguments()
    main(parmeter.time)
