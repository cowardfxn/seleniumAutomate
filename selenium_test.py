#!/usr/bin/python3
# encoding: utf-8

import os, sys
if sys.platform == "darwin":
    pass
os.environ["PATH"] += ":{}".format(os.path.abspath("./lib"))


from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def firefox_test():
    browser = webdriver.Firefox()

    main_url = "https://www.bing.com"
    browser.get(main_url)
    assert "bing" in browser.title

    q_input = browser.find_element_by_id('sb_form_q')
    q_input.send_keys("1345234" + Keys.RETURN)

    browser.quit()


def chrome_test():
    browser = webdriver.Chrome()
    try:
        # timeout时间为10s
        wait = WebDriverWait(browser, 10)

        homepage = "http://localhost:13000"
        browser.get(homepage)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-success btn-lg"]')))

        browser.find_element_by_name('username').clear()
        browser.find_element_by_name('username').send_keys("fantest")
        browser.find_element_by_name('password').clear()
        browser.find_element_by_name('password').send_keys("12345")
        browser.find_element_by_tag_name('button').click()

        sleep(5)
        browser.find_element_by_xpath('//a[@href="/Report"]').click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#WindRose")))

        # browser.get("http://localhost:13000/Report")
        browser.find_element_by_id("WindRose").click()
        # wait
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[name="TurbineCheckBox"]')))
        # 单选
        browser.find_element_by_id("F0050001001").click()
        # 下拉框处理，需要先点击本体，再点击选项
        ActionChains(browser).click(browser.find_element_by_id("reportSelect")).perform()
        browser.find_element_by_css_selector('option[value="months"]').click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#StartDate")))

        browser.find_element_by_id("StartDate").send_keys("2015-01")

        # 序号从1开始
        browser.find_element_by_xpath("//div[@id='infoPanel']/button[1]").click()
        # 表格查询
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.odd")))
        browser.get_screenshot_as_file("/Users/fanxn/Desktop/1233443.png")

        # ss = browser.get_screenshot_as_png()
    finally:
        browser.close()
        browser.quit()


def save_into_excel(file_name, data):
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image
    try:
        from PIL import Image as PILImage
    except ImportError as ime:
        print(ime)
        print("PIL should be installed!")
        return

    wb = Workbook()
    ws=wb.active
    ws["A1"]="图片1"
    img = Image("/Users/fanxn/Desktop/1233443.png")
    ws.add_image(img, "A1")
    wb.save(file_name)


if __name__ == '__main__':
    chrome_test()
