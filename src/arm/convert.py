import csv
import re
import pandas


def is_valid_format_date(_date):
    regex = r"\d{2}-\d{2}-\d{4}\s\d{2}:\d{2}:\d{2}"
    return bool(re.match(regex, _date))


def found_cpu_temp(contents):
    for content in contents:
        if content.startswith("CPU@"):
            return content[4:]
    return -1


def found_gpu_temp(contents):
    for content in contents:
        if content.startswith("GPU@"):
            return content[4:]
    return -1


def load_content():
    day_list = []
    cpu_temp = []
    gpu_temp = []
    try:
        file = open("../../data/jetpack.txt", "r")
        lines = file.readlines()
        for line in lines:
            content = list(line.split(" "))
            date = content[0] + " " + content[1]
            if is_valid_format_date(date):
                day_list.append(date)
                cpu_temp.append(found_cpu_temp(content))
                gpu_temp.append(found_gpu_temp(content))
        return day_list, cpu_temp, gpu_temp

    except:
        print("data folder didn't have jetpack.txt")


def save_file():
    date_list, cpu_list, gpu_list = load_content()
    try:
        df = pandas.read_csv("../../data/computer_information.csv")
        if len(cpu_list) == len(df):
            df.insert(0, "CPU Temperature", cpu_list)
            df.insert(1, "GPU Temperature", gpu_list)
            df.to_csv("../../data/total_info.csv")
            print("saved the total_info.csv file")
        else:
            if cpu_list and gpu_list:
                first_day = date_list[0]
                data = [cpu_list[0], gpu_list[0]]
                new_df = pandas.DataFrame(
                    data=[data],
                    index=[first_day],
                    columns=["CPU Temperature", "GPU Temperature"],
                )
                new_df.to_csv("../../data/temperature.csv")
                for i in range(1, len(date_list)):
                    index = date_list[i]
                    new_df.loc[index] = [cpu_list[i], gpu_list[i]]
                    new_df.to_csv("../../data/temperature.csv")
                print(
                    "saved the CPU temperature and GPU temperature in temperature.csv file"
                )
    except:
        print("data folder didn't have computer_information.csv")


def main():
    save_file()


if __name__ == "__main__":
    main()
