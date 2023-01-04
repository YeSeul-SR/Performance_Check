import os
import argparse
import sys
import time
import psutil
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

def check_CPU_info():
    usage = psutil.cpu_percent(interval=None)
    temp = [usage]
    label = ["usage"]
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

def check_etc_usage():
    info = []

    load_memory = psutil.virtual_memory()
    info.append(load_memory[2])

    load_disk = psutil.disk_usage('/')
    info.append(load_disk.percent)

    return info

def check_network():
    label = []
    status = []
    stats = psutil.net_if_stats()
    for nic, addrs in psutil.net_if_addrs().items():
        if nic in stats:
            label.append(nic + ": IPv4")
            status.append(addrs[1].address)
            label.append(nic+": status")
            status.append(stats[nic].isup)
    return label, status

def parse_arguments():
    parser = argparse.ArgumentParser(description="Enter the time in seconds.")
    parser.add_argument('--time', type=int, default=30)
    return parser.parse_args()

def save_file(GPU_df,CPU_df,usage_df, network_df):
    GPU_df.to_csv("./data/GPU.csv")
    CPU_df.to_csv("./data/CPU.csv")
    usage_df.to_csv("./data/usage_info.csv")
    network_df.to_csv("./data/network.csv")

def main(timer):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{date} start to check LPU-B status")
    GPU_df = pandas.DataFrame(check_GPU_info(), columns=[date], index=["temperature", "usage", "memory usage"])
    cpu_label, cpu_info = check_CPU_info()
    CPU_df = pandas.DataFrame(cpu_info, columns=[date], index=cpu_label)
    usage_df = pandas.DataFrame(check_etc_usage(), columns=[date], index=["memory", "disk"])
    net_label, net_status = check_network()
    network_df = pandas.DataFrame(net_status, columns=[date], index=net_label)
    save_file(GPU_df,CPU_df,usage_df, network_df)
    time.sleep(timer)

    while True:
        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        GPU_df[date] = check_GPU_info()
        cpu_name, cpu_info = check_CPU_info()
        CPU_df[date] = cpu_info
        usage_df[date] = check_etc_usage()
        net_label, net_status = check_network()
        network_df = pandas.DataFrame(net_status, columns=[date], index=net_label)

        save_file(GPU_df,CPU_df,usage_df,network_df)
        print(f"{date}, saved file")

        time.sleep(timer)


if __name__ == '__main__':
    parmeter = parse_arguments()
    main(parmeter.time)
