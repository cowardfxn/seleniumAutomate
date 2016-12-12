# Selenium自动化测试框架
Automated selenium test framework

*Powered by fanxn*

## 环境要求 Requirements

 - Python3+
 - selenium
 - chromedriver
 - openpyxl
 - Chrome 52.0+ or Firefox
 - pillow

## 说明 Description
运行 `python start.py`启动测试
程序会读取Scenarios目录下的所有用例定义文件，按顺序执行文件中定义的动作
如果在用例定义文件中定义了截图操作，截图会被保存在在target目录下，按照用例文件名命名的目录中。

Run command `python start.py` will automatically read scenario definition files in directory "Scenarios",
execute scenarios sequentially. If saving screenshot is ordered, screenshot will be saved in a directory
named after the scenario file name in directory "target".

v0.1 改动
1. 添加滚动截图功能，如果页面长度超过屏幕显示，那么同一页面将会产生多张截图，然后被合并为一张进行存储。

