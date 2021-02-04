# -*- coding: utf-8 -*-
"""
@Time       : 2020/9/28 14:48
@Author     : 杜权
@File       ：pil_selenium
@Description:
"""
import logging
import os
import sys
import time
import traceback

from lxml import etree
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)

from utils.util_selenium import SeleniumSpiderBase
#from utils.util_mail import UtilSendEmail
#from utils.util_data_interaction import UtilData
#from utils import config
#from utils.config import SERVER_ENV

#log_file_path = os.path.join(PROJECT_PATH, "logs", "pil_selenium.log")
#logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Yearningselenium(SeleniumSpiderBase):
    def __init__(self):
        super(Yearningselenium, self).__init__()
        self.company = "PIL"
        #self.set_pid(company=self.company)
        self.is_headless = True
        self.use_virtualdisplay = False
        self.url = "http://yearning.hgj.net/"
        self.remark = ""

    def get_web_index(self):
        """打开页面"""
        while True:
            try:
                # 没有获取到提单号输入框，请求url
                self.browser.get(self.url)
            except:
                time.sleep(10)
                continue

            while True:
                try:
                    page_source = self.browser.page_source
                    time.sleep(10)
                    page_source = self.browser.page_source
                    break
                except:
                    continue

            if "The requested URL was rejected." in page_source or 'VGM Declaration' not in page_source:
                self.browser.quit()
                self.print_log("The requested URL was rejected. 三分钟后重试")
                time.sleep(60 * 3)
                self.browser = self.create_browser(is_headless=self.is_headless, use_virtualdisplay=self.use_virtualdisplay)
                continue

            try:
                WebDriverWait(self.browser, 20, 0.5).until(EC.element_to_be_clickable((By.ID, 'refnumbers')))
                self.print_log("加载页面成功")
                return True
            except:
                continue

    def get_container_table(self, vgm_info):
        """输入Booking_Number，点击搜索"""
        Booking_Number = vgm_info['billOfLadingNo']  # 订舱号
        times= 0
        while True:
            try:
                times += 1
                # Booking_Number
                self.browser.find_element_by_id('refnumbers').clear()
                time.sleep(1)
                self.print_log("输入提单号并点击搜索")
                self.click_and_send_keys(self.browser, 'id', 'refnumbers', Booking_Number)
                time.sleep(1)

                # 监测是否有错误信息提示
                self.browser.find_element_by_id('button').click()
                # 执行js点击
                for i in range(30):
                    try:
                        info_element = self.browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/span')
                        self.browser.execute_script("arguments[0].click();", info_element)
                        break
                    except:
                        time.sleep(0.5)
                        try:
                            self.browser.find_element_by_id('email').click()
                            return True
                        except:
                            pass

                page_source = self.browser.page_source
                if 'VGM Declaration' not in page_source or times >= 3:
                    times = 0
                    self.browser.quit()
                    time.sleep(60 * 2)
                    self.browser = self.create_browser(is_headless=self.is_headless, use_virtualdisplay=self.use_virtualdisplay)
                    continue
                else:
                    html_element = etree.HTML(page_source, etree.HTMLParser(encoding="utf-8"))
                    info = ''.join(html_element.xpath('/html/body/div[2]/div/div[4]//text()')).strip()
                    if info in ['Please enter reference number', ""]:
                        # 没有输入提单号
                        continue
                    else:
                        # 其他错误，如：提单号错误  Invalid reference number
                        self.remark = info
                        return -1
            except:
                self.get_web_index()

    def upload_one(self, vgm_info):
        """上传"""
        Booking_Number = vgm_info['billOfLadingNo']  # 订舱号
        Container_Number = vgm_info['containerNo']  # 箱号
        weight = vgm_info['weight']  # VGM
        Authorized_Person = vgm_info['sign']  # 签名
        VGM_EMAIL = "cs.vgm@yunlsp.com"  # 电子邮件

        retry = 0
        retry_flag = False
        container_count = 0
        while True:
            flag = self.get_container_table(vgm_info)
            if flag == -1:
                return False

            try:
                try:
                    self.click_and_send_keys(self.browser, 'id', 'email', VGM_EMAIL)
                    time.sleep(1)
                except:
                    self.print_log("输入email失败，一分钟后重试")
                    time.sleep(60)
                    try:
                        self.browser.quit()
                    except:
                        pass
                    self.browser = self.create_browser(is_headless=self.is_headless, use_virtualdisplay=self.use_virtualdisplay)
                    continue

                # 获取所有的箱子，并定位到对应的那一行
                html_element = etree.HTML(self.browser.page_source, etree.HTMLParser(encoding="utf-8"))
                Container_Number_list = html_element.xpath('//*[@id="ref_info_main"]/tr/td[1]/input/@value')
                try:
                    Container_Number_list.remove('')
                except:
                    pass
                try:
                    if len(Container_Number_list) == 0:
                        self.print_log("当前页面没有获取到任何箱号")
                        if container_count >= 1:
                            self.remark = "没有找到对应的箱号"
                            return False
                        container_count += 1
                        time.sleep(60)
                        continue

                    index = Container_Number_list.index(Container_Number) + 2  # 元素对应位置要 + 1
                except:
                    self.remark = "没有找到对应的箱号"
                    self.print_log(f"当前页面获取到的箱号：{''.join(Container_Number_list)}, 没有找到对应的箱号")
                    return False

                try:
                    # 滚动至元素位置
                    ele = self.browser.find_element_by_css_selector(f'#ref_info_main > tr:nth-child({index}) > td:nth-child(2) > input')
                    self.browser.execute_script("arguments[0].scrollIntoView();", ele)
                    time.sleep(1)

                    # 输入重量
                    self.click_and_send_keys(self.browser, 'css', f'#ref_info_main > tr:nth-child({index}) > td:nth-child(2) > input', weight)
                    time.sleep(1)

                    # 选择日期
                    self.browser.find_element_by_css_selector(f'#ref_info_main > tr:nth-child({index}) > td:nth-child(4) > input').click()
                    time.sleep(0.5)
                    self.browser.find_element_by_css_selector(f'#ref_info_main > tr:nth-child({index}) > td:nth-child(4) > input').send_keys(Keys.ENTER)
                    time.sleep(1)

                    # 负责人
                    self.click_and_send_keys(self.browser, 'css', f'#ref_info_main > tr:nth-child({index}) > td:nth-child(5) > input.txtSign', Authorized_Person)
                    time.sleep(1)

                    ele = self.browser.find_element_by_css_selector(f'#ref_info_main > tr:nth-child({index}) > td:nth-child(5) > input.txtSign')
                    self.browser.execute_script("arguments[0].scrollIntoView();", ele)

                    self.browser.find_element_by_id('saveVGM').click()
                except:
                    self.print_log("输入VGM信息时错误")
                    time.sleep(60)
                    continue

                while True:
                    try:
                        page_source = self.browser.page_source
                    except:
                        continue

                    if Container_Number in page_source:
                        # 点击保存
                        try:
                            self.browser.find_element_by_id('saveVGM').click()
                            continue
                        except:
                            pass
                    elif Booking_Number not in page_source:
                        return True
                    else:
                        retry_flag = True
                        break

                if retry_flag is True:
                    continue
            except:
                self.print_log(traceback.format_exc())
                retry += 1
                if retry >= 3:
                    self.util_email.send_email(to="duke.du@yunlsp.com", subject='Reject：PIL 上传程序错误', contents=["上传程序连续错误三次", "程序将睡眠半个小时，请速核查", traceback.format_exc()])
                    time.sleep(60 * 30)
                time.sleep(60)

    def get_vgm_info(self):
        """每次最多取十个，运行结束约半个小时，关闭一次浏览器"""
        while True:
            vgm_info_list = self.util_data.get_data(self.company, count=50)
            if len(vgm_info_list) == 0:
                time.sleep(60)
                continue
            return vgm_info_list

    def run(self):
        while True:
            self.browser = self.create_browser(is_headless=self.is_headless, use_virtualdisplay=self.use_virtualdisplay)
            print(self.browser.__dict__)
            #self.browser.get(self.url)
            #self.browser.save_screenshot(os.path.abspath('') + "\\out\\test.jpg")
            #self.browser.quit()





if __name__ == '__main__':
    practice = Yearningselenium()
    practice.run()
