
import datetime
import json
import logging
import os
import platform
import sys
import time
import string
import traceback
import zipfile
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

from xlutils.copy import copy
import xlrd



class SeleniumSpiderBase(object):
    def __init__(self,):
        self.a = 1
    def create_browser(self, is_headless=False, use_proxy=False, use_virtualdisplay=False):
        chrome_options = webdriver.ChromeOptions()
        if use_virtualdisplay:
            from pyvirtualdisplay import Display
            # 使用虚拟窗口
            self.display = Display(visible=0, size=(1792, 1120))
            self.display.start()
            is_headless = False  # 其实是有界面的

            # chrome_options.add_argument('window-size=1920x1080')  # 指定分辨率
        chrome_options.add_argument('--no-sandbox')  # root
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])  # 取消chrome受自动控制提示

        # chrome_options.add_argument("--disable-extensions")  # 扩展程序
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

        # 关掉密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        chrome_options.add_experimental_option("prefs", prefs)

        ip_key = ""
        if is_headless is True:
            chrome_options.add_argument('--headless')

        #while True:
        try:
            if platform.system() in ['Darwin', 'Linux','Windows']:
                browser = webdriver.Chrome(executable_path=os.path.abspath('')+"\\browser\\chromedriver.exe", options=chrome_options)
            else:
                browser = webdriver.Chrome(executable_path=os.path.abspath('')+"\\browser\\chromedriver.exe", options=chrome_options)

        except WebDriverException:
            return Exception


    # try:
    #     tk = tkinter.Tk()
    #     width = tk.winfo_screenwidth()
    #     height = tk.winfo_screenheight()
    #     tk.quit()
    # except:
        width = 1792
        height = 1120
        browser.set_window_size(width, height)

        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        return browser

    def click_and_send_keys(self, browser, by, value, msg):
        """
        点击并发送
        每次都获取是因为有时旧的元素定位不到会报错，所以每次都重新获取元素并完成相应操作
        """
        self.__get_element(browser, by, value).click()
        time.sleep(1)
        self.__get_element(browser, by, value).clear()
        self.__get_element(browser, by, value).click()
        time.sleep(1)
        self.__get_element(browser, by, value).send_keys(msg)

    def hover(self, browser, by, value):
        """鼠标悬浮"""
        element = self.__get_element(browser, by, value)
        ActionChains(browser).move_to_element(element).perform()

    def write_excel_xls_append(self, path, value):
        """
        追加入需要上传的excel中
        :param path:
        :param value:
        :return:
        """
        try:
            index = len(value)  # 获取需要写入数据的行数
            workbook = xlrd.open_workbook(path)  # 打开工作簿
            sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
            worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
            rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
            for i in range(0, index):
                for j in range(0, len(value[i])):
                    new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
            new_workbook.save(path)  # 保存工作簿
            self.print_log(f"excel文件写入成功：{index}箱")
        except Exception as e:
            raise e




    def __get_element(self, browser, by, value):
        """通过不同的方式查找界面元素"""
        element = None
        by = by.lower()
        if (by == "id"):
            element = browser.find_element_by_id(value)
        elif (by == "name"):
            element = browser.find_element_by_name(value)
        elif (by == "xpath"):
            element = browser.find_element_by_xpath(value)
        elif (by == "classname"):
            element = browser.find_element_by_class_name(value)
        elif (by == "css"):
            element = browser.find_element_by_css_selector(value)
        elif (by == "link_text"):
            element = browser.find_element_by_link_text(value)
        else:
            print("无对应方法，请检查")
        return element

    @staticmethod
    def set_pid(company):
        """设置pid"""
        with open(os.path.join(os.path(''), "out", "pid.txt"), "a+") as f:
            pid = str(os.getpid())
            f.write(company.lower() + "=" + pid + "\n")

    @staticmethod
    def print_log(msg, level=logging.INFO):
        logging.log(level, msg)
        print("【{}】{}".format(datetime.datetime.now(), msg))
