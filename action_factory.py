#!/usr/bin/python
# encoding: utf-8

import os

os.environ["PATH"] += ":{}".format(os.path.abspath("./lib"))

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from PIL import Image
from io import BytesIO


# 定义选择方式
class Selector:
    def __init__(self, browser):
        self.browser = browser

    def get(self, selector_type, descriptor):
        if selector_type == "CSS选择器":
            selector = self.browser.find_element_by_css_selector
        elif selector_type == "name属性":
            selector = self.browser.find_element_by_name
        elif selector_type == "指定ID":
            selector = self.browser.find_element_by_id
        elif selector_type == "XPATH":
            selector = self.browser.find_element_by_xpath
        elif selector_type == "标签名":
            selector = self.browser.find_element_by_tag_name
        else:
            selector = self.browser.find_element

        try:
            return selector(descriptor)
        except WebDriverException as wde:
            self.browser.quit()
            raise wde


class Action:
    def __init__(self):
        self.browser = ""
        self.wait = ""
        self.selector = ""

    # 开始
    def begin(self, type="chrome"):
        if type.lower() == "firefox":
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.selector = Selector(self.browser).get

    # 结束
    def end(self):
        self.browser.quit()

    # 点击
    def click(self, selector_type, descriptor):
        self.selector(selector_type, descriptor).click()

    # 输入
    def enter(self, selector_type, descriptor, context):
        self.selector(selector_type, descriptor).send_keys(context)

    # 清空
    def clear(self, selector_type, descriptor, context):
        self.selector(selector_type, descriptor).clear()

    # URL跳转
    def goto_url(self, url):
        self.browser.get(url)

    # 截图
    def save_img(self, dir_name, img_name, path="./target"):
        path = os.path.join(path, dir_name)
        if not os.path.exists(path):
            os.mkdir(path)

        if not (img_name.endswith(".png") or img_name.endswith(".jpg") or img_name.endswith(".git")):
            img_name = "{}.png".format(img_name)
        img_path = os.path.abspath(os.path.join(path, img_name))
        # print("Image saved at {}".format(img_path))
        # self.browser.get_screenshot_as_file(img_path)
        get_scroll_screenshot(self.browser, img_path)

    # 等待
    def waiting(self, selector_type, descriptor, timeout):
        if timeout is not None and type(timeout) == int:
            self.wait = WebDriverWait(self.browser, timeout)

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, descriptor)))

    # 异常退出时处理
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 重复quit不会出错
        self.end()


# 滚动截图
def get_scroll_screenshot(browser, img_path):
    # 整个页面的高度
    whole_page_height = browser.execute_script("return document.body.clientHeight;")
    # 当前窗口页面高度
    single_window_height = browser.execute_script("return window.innerHeight;")

    # 截图，保存为bytes格式数据
    raw_pngs = []
    cur_height = 0
    browser.execute_script("window.scrollTo(0, {});".format(cur_height))
    raw_pngs.append(browser.get_screenshot_as_png())
    img_first = Image.open(BytesIO(raw_pngs[0]))
    single_size = img_first.size
    cur_height += single_window_height
    while cur_height <= whole_page_height:
        browser.execute_script("window.scrollTo(0, {});".format(cur_height))
        raw_pngs.append(browser.get_screenshot_as_png())
        cur_height += single_window_height

    # 将所有截图合并
    img_all = Image.new("RGB", (single_size[0], single_size[1] * len(raw_pngs)))
    height_shift = 0
    img_all.paste(img_first, (0, height_shift))
    for raw_png in raw_pngs[1:]:
        height_shift += single_size[1]
        img_tmp = Image.open(BytesIO(raw_png))
        img_all.paste(img_tmp, (0, height_shift))
    # img_all.show()
    # 保存为文件
    img_all.save(img_path, format="png")
    print("Image saved at {}".format(img_path))
