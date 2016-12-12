#!/usr/bin/python
# encoding: utf-8

# 读取用例定义文件，运行相应测试，并保存测试结果

import os.path
from openpyxl import load_workbook
from action_factory import Action
from time import sleep


def usercase_proc(filename):
    # Additional keyword args(read_only, data_only) to avoid warning messages
    wb = load_workbook(filename=filename, read_only=True, data_only=True)

    ws = wb.worksheets[0]
    lines = list(ws.rows)
    START_POS = (4, 3)
    action = Action()
    for line in lines[START_POS[0]:]:
        # 去掉说明列
        action_name, selector_type, descriptor, item_type, cont = [e.value for e in line[START_POS[1]:]]
        # print(action_name, selector_type, descriptor, item_type, cont)

        if action_name == "开始":
            action.begin()
        elif action_name == "点击":
            action.click(selector_type, descriptor)
        elif action_name == "输入":
            action.enter(selector_type, descriptor, cont)
        elif action_name == "清空":
            action.clear(selector_type, descriptor, cont)
        elif action_name == "截图":
            dir_name = os.path.basename(filename).split(".")[0]
            action.save_img(dir_name, cont)
        elif action_name == "URL输入":
            action.goto_url(cont)
        elif action_name == "等待":
            if cont is not None:
                cont = int(cont)
            action.waiting(selector_type, descriptor, cont)
        elif action_name == "结束":
            action.end()
        elif action_name is None:
            break

        # 迷信 防止程序卡顿
        sleep(1)
