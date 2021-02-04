from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from bs4 import BeautifulSoup
import requests





driver=Chrome(os.path.abspath('')+"\\browser\\chromedriver.exe")
driver.set_window_size(1280,1080)

driver.implicitly_wait(3)
url='http://yearning.hgj.net/#/login'

driver.get(url)
print(1,driver.current_url)
time.sleep(3)
driver.save_screenshot(os.path.abspath('') + "\\out\\test.png")
#driver.save_screenshot('d:/text.png')

with requests.Request(method="GET",url=url) as e:
      print(e)


#
if __name__ == '__main__':
      #driver.find_element_by_class_name('sms-login-tab-item').click()


      username = driver.find_element_by_class_name('ivu-icon-md-key')

      #username.send_keys(input('请输入您账号'))
      username.send_keys('admin')
      password=driver.find_element_by_class_name('ivu-icon ivu-icon-md-key')
      time.sleep(2)
      #driver.find_element_by_class_name('send-btn').click()
      password.send_keys('ldap123')
      #driver.find_element_by_class_name('password-login').click()
      time.sleep(2)
      print(os.path.abspath('') + "\\out\\test.jpg")
      driver.save_screenshot(os.path.abspath('') + "\\out\\test.jpg")

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