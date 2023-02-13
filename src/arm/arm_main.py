import os
import argparse
import time
import psutil
import pandas
from datetime import datetime


def check_etc_usage():
    info = []

    info.append(psutil.cpu_percent(interval=None))

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
    now = timestamp.strftime("%m-%d-%Y %H:%M:%S")

    column = []
    data = []

    usage_info = check_etc_usage()
    column.append("CPU Usage")
    column.append("Memory Usage")
    column.append("Disk Usage")
    for info in usage_info:
        data.append(info)

    net_label, net_status = check_network()
    for label in net_label:
        column.append(label)
    for status in net_status:
        data.append(status)

    return now, data, column


def check_cpu_gpu_temperature(timer):
    return os.popen(
        f"tegrastats --interval {timer*1000} --logfile ../../data/cpu_gpu_temperature.txt"
    )


def save_file(df):
    now, data, column = get_data()
    df.loc[now] = data
    if not os.path.exists("../../data/computer_information.csv"):
        df.to_csv("../../data/computer_information.csv", index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv("../../data/computer_information.csv", index=False, mode='a', encoding='utf-8-sig', header=False)
    print(f"{now}, saved to file")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Enter the time in seconds.")
    parser.add_argument("--time", type=int, default=30)
    return parser.parse_args()


def main(timer):
    print("starting checked the performance")

    check_cpu_gpu_temperature(timer)
    time.sleep(timer)

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
