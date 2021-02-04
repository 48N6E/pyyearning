from selenium.webdriver import PhantomJS,Chrome
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from email.header import Header
import smtplib


chrome_options = webdriver.ChromeOptions()

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

chrome_options.add_argument('--headless')

driver=Chrome(os.path.abspath('')+"\\browser\\chromedriver.exe",options=chrome_options)
driver.set_window_size(1280,1080)

url='http://yearning.hgj.net/#/login'
url = 'http://10.10.10.198:8000'
driver.get(url)

driver.save_screenshot(os.path.abspath('') + "\\out\\test.png")



def signUp():
      username = driver.find_element_by_xpath('//input')
      username.send_keys('admin')

      password = driver.find_element_by_xpath('//input[@placeholder="密码"]')
      password.send_keys('admin123')
      # driver.find_element_by_class_name('password-login').click()
      password.send_keys(Keys.ENTER)
      #driver.save_screenshot(os.path.abspath('') + "\\out\\test2.png")



def readdetail():
      #driver.find_element_by_xpath('//span[@class="layout-text"]')
      signUp()
      time.sleep(1)
      flag = 1
      try:
            print("点击审核")
            driver.find_element_by_xpath("//span[contains(.,'审核')]").click()
            flag = 0
            if  flag == 0  :
                  time.sleep(1)
                  driver.save_screenshot(os.path.abspath('') + "\\out\\test2.png")
                  print("点击工单")
                  #// input[ @class ="s_ipt" and @ name="wd"]
                  driver.find_element_by_xpath("//div[last()-2]//ul/li[1]/span[contains(.,'工单')]").click()
                  time.sleep(1)
                  driver.save_screenshot(os.path.abspath('') + "\\out\\test2.png")
            else:
                  driver.quit()
      except:
            print("没找到工单")
            driver.quit()


def select_job():
      readdetail()
      flag = 0
      driver.find_element_by_xpath("//button[contains(.,'审批')]").click()
      driver.save_screenshot(os.path.abspath('') + "\\out\\test2.png")
      flag = 1


def sendMail(content,from_addr= '2278562@qq.com',to_addr= 'denis.mao@yunlsp.com',title='python test',smtp_server='smtp.qq.com'):
    # 用于构建邮件头
    msg = MIMEText(content, 'html', 'utf-8')
    print(from_addr)

    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(title)
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '2278562@qq.com'
    password = 'gjkiwcwsunkecbdg'
    # 发信服务器
    #smtp_server =
    # 收信方邮箱
    to_addr = 'denis.mao@yunlsp.com'
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, content.as_string())
    # 关闭服务器
    server.quit()


if __name__ == '__main__':
      #driver.find_element_by_class_name('sms-login-tab-item').click()
      while True:
            select_job()

      #driver.find_element_by_class_name('send-btn').click()
      #password.send_keys(input('请输入验证码'))
      #time.sleep(2)
     #password.send_keys(Keys.ENTER)

      #driver.save_screenshot(os.path.abspath('')+"\\out\\test.jpg")

#     key_word = input('请输入您想搜索的关键词：')
#     num = int(input('请输入您想检索的次数：')) + 1
#     sleep_time = int(input('请输入每次检索延时的秒数：'))
#     key_word = urllib.parse.quote(key_word)
#
#     print('正在搜索，请稍后')