#!/usr/bin/python
# encoding: utf-8

import os
from time import strftime, localtime
from scenarion_factory import usercase_proc


def run_test():
    time_format = "%Y-%m-%d %H:%M:%S"
    for dir_name, sub_dir, filenames in os.walk("./Scenarios"):
        for filename in filenames:
            filename = os.path.abspath(os.path.join(dir_name, filename))
            print("Process of scenario file {} starts at {}".format(filename, strftime(time_format, localtime())))
            usercase_proc(filename)
            print("Process of scenario file {} ends at {}".format(filename, strftime(time_format, localtime())))


if __name__ == "__main__":
    run_test()
