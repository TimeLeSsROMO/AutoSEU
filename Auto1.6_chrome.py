from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.chrome.options import Options
from datetime import date, timedelta
import time
import random
import json
import re


# 加启动配置 禁用日志log
chrome_options = Options()
# “–no - sandbox”参数是让Chrome在root权限下跑
chrome_options.add_argument('–no-sandbox')
chrome_options.add_argument('–disable-dev-shm-usage')
chrome_options.add_experimental_option(
    'excludeSwitches', ['enable-automation'])
chrome_options.add_argument('--start-maximized')  # 最大化
chrome_options.add_argument('--incognito')  # 无痕隐身模式
chrome_options.add_argument("disable-cache")  # 禁用缓存
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--headless')

url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/*default/index.do"
enter_campus_url = "http://ehall.seu.edu.cn/ygfw/sys/swmxsqjappseuyangong/*default/index.do#/"  # 申请入校网址
dailyDone1 = False

# 创建打卡记录log文件

def writeLog(text):
    with open('log.txt', 'a') as f:
        s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + text
        print(s)
        f.write(s + '\n')
        f.close()

# 创建账号密码文件，以后都不用重复输入
def getUserData():
    # 读取账号密码文件
    try:
        with open("loginData.json", mode='r', encoding='utf-8') as f:
            # 去掉换行符
            loginData = f.readline()
            f.close()

    # 写入账号密码文件
    except FileNotFoundError:
        print(" ")
        print("Welcome to do THE F***ING DAILY JOB automatically in Southeast University")
        print(" ")
        print("Copyrights belong to Everyone who Suffers this Hardship")
        print(" ")
        print("Tips：请确保在现版系统中进行过至少一次健康申报和出校审批，否则可能出现奇怪的错误导致无法正常运行")
        print("      各种问题可以联系TimeLeSs，如果你可以联系到我的话~_~")
        print(" ")
        with open("loginData.json", mode='w', encoding='utf-8') as f:
            user = input('输入一卡通号: ')
            pw = input('输入密码: ')
            n1 = input('输入家人姓名: ')
            T1 = input('输入家人电话号码: ')
            n2 = input('输入辅导员姓名: ')
            T2 = input('输入辅导员电话号码: ')
            reas = input('输入请假原因: ')
            adres = input('输入校园地址: ')
            loginData = {"username": user, "password": pw, "name1": n1, "TN1": T1, "name2": n2, "TN2": T2, "reason": reas, "adress": adres,
                         "loc": ""}
            loginData = json.dumps(loginData) + '\n'
            f.write(loginData)
            f.close()

    return loginData

# 检查是否已经超过健康申报时间
def checkTime():
    localtime = time.localtime(time.time())
    hour = localtime.tm_hour  
    minite = localtime.tm_min

    if hour >= 15:   # 超过15:00则无法进行健康申报（程序运行也需要一点时间
        return True
    else:
        return False
        
# 检查是否已经超过出校审批时间
def checkTime2():
    localtime = time.localtime(time.time())
    hour = localtime.tm_hour  
    minite = localtime.tm_min

    if hour >= 16:   # 超过16:00则出校审批可能无法通过（程序运行也需要一点时间
        return True
    else:
        return False

def login(user, pw, browser):
    browser.get(url)
    browser.implicitly_wait(5)

    # 填写用户名密码
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    username.clear()
    password.clear()
    username.send_keys(user)
    password.send_keys(pw)

    # 点击登录
    login_button = browser.find_element_by_class_name('auth_login_btn')
    login_button.submit()
    
# 检查是否无text按钮
def check(text, browser):
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        if button.get_attribute("textContent").find(text) >= 0:
            return True
    return False

# 定义时间
today_year = date.today().strftime("%Y")
today_month = date.today().strftime("%m")
today_day = date.today().strftime("%d")
tomorrow_year = (date.today() + timedelta(days=1)).strftime("%Y")
tomorrow_month = (date.today() + timedelta(days=1)).strftime("%m")
tomorrow_day = (date.today() + timedelta(days=1)).strftime("%d")
tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

# 确认是否健康申报成功
def dailyDone():
    browser.get(url)
    browser.implicitly_wait(5)
    time.sleep(5)

    date_info_raw = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div[2]")
    date_info = re.findall(r"\d+\.?\d*",date_info_raw.text)
    year_info = date_info[0]
    month_info = date_info[1]
    day_info = date_info[2]

    if year_info == today_year and month_info == today_month and day_info == today_day:
        return True
    else:
        return False

# 检查第二日入校是否已申请
def checkEnterCampus(browser):
    try:
         browser.get(enter_campus_url)
         browser.implicitly_wait(5)
         time.sleep(5)

         date_info2_raw = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div")
         date_info2 = re.findall(r"\d+\.?\d*",date_info2_raw.text)
         year_info2 = date_info2[0]
         month_info2 = date_info2[1]
         day_info2 = date_info2[2]

         if year_info2 == tomorrow_year and month_info2 == tomorrow_month and day_info2 == tomorrow_day:
             return True
         else:
             return False
    except:
    	       return Error
    	       print("------------网站出现故障，请稍候重试----------------")

def checkpassed(browser):
    time.sleep(2)
    print('正在检查明日的出校审批是否通过')
    browser.get(enter_campus_url)
    browser.implicitly_wait(5)
    time.sleep(5)    
    try:
         if browser.find_element(By.XPATH, '//html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div[contains(text(), "已通过")]'):
              return True
         else:
              return False
    except:
         return False

def IFF():
    if checkpassed(browser) == True:
        print('恭喜，明日的出校审批已通过，如有问题可自行进入学校系统查看')
        browser.quit()
        print('-------------------后台已关闭----------------------')
        print('本次运行结束，本窗口将在10秒后自动关闭，再见~')
        time.sleep(10)
        exit()
    elif checkpassed(browser) == False:
        print('出校审批暂未通过，请稍候自行进入学校系统查看')
        browser.quit()
        time.sleep(1)                 	   
        print("-------------------后台已关闭----------------------")
        print("本次运行结束，本窗口将在10秒后自动关闭，再见~")
        time.sleep(10)
        exit()

# 开始申请第二日入校
def sqxj():
    browser.get(enter_campus_url)
    browser.find_element_by_class_name('mint-button').click()
    time.sleep(2)
    js = "document.querySelector(\"#app > div > div > div:nth-child(5) > button\").click();"
    browser.execute_script(js)
    time.sleep(2)
    browser.find_element_by_class_name('mint-msgbox-confirm').click()
    time.sleep(2)
def checksqxj():
    browser.get(enter_campus_url)
    try:
         if browser.find_element_by_class_name('mint-button'):
              return True
         else:
              return False
    except:
    	   return False
    	
def enterCampus(browser):
    # 询问是否继续
    print(' ')
    print("健康申报进程已结束，请确认是否继续进行明日的出校审批！")
    print("注意！此操作会注销目前所有的出校审批（包含本日），可能会导致本日剩余时间为无效卡，请确认！！！")
    qt2 = str(input("输入“Y”继续，或输入“N”退出: "))                
    if qt2 == "N":
         browser.quit()
         print('本次运行结束，本窗口将在10秒后自动关闭，再见~')
         time.sleep(10)
         exit(0)
    elif qt2 == "Y":
         print(' ')
         print('运行中，请稍候')
         if checkTime2() == True:
              print(' ')
              print('注意，规定的出校审批最晚时间已过，明日出校审批可能无法通过')
         if checkTime2() == False:
              print(' ')
              print('目前是出校审批的申请时间段')         
         # 检查今天是否已申请
         if checkEnterCampus(browser) == True:
              print(' ')
              print('已申请过明日的出校审批，如有问题可自行进入学校系统查看，即将检查审批是否通过')
              checkpassed(browser)
              IFF()
         elif checkEnterCampus(browser) == False:
              browser.get(enter_campus_url)
              print(' ')
              print('未进行明日的出校审批，开始运行')
              browser.implicitly_wait(10)
              time.sleep(10)

              # 进行销假后才可以申请
              checksqxj()
              while checksqxj() == True:
                    print('有未销假记录，正在销假')
                    sqxj()
                    time.sleep(5)
                    checksqxj()
                    time.sleep(5)
                    if checksqxj() == False:
                        break
          
              # 点击加号
              js = "document.querySelector(\"#app > div > div > div.mint-fixed-button.mt-color-white.sjarvhx43.mint-fixed-button--bottom-right.mint-fixed-button--primary.mt-bg-primary\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 通过须知
              js = "document.querySelector(\"#CheckCns\").click();"
              browser.execute_script(js)
              time.sleep(1)
              
              js = "document.querySelector(\"body > div.mint-msgbox-wrapper > div > div.mint-msgbox-btns > button.mint-msgbox-btn.mint-msgbox-confirm.mt-btn-primary\").click();"
              browser.execute_script(js)
              time.sleep(1)

              #####################################################################################
              # 家长信息填写
              input_box = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[6]/div/a/div[2]/div[2]/input")
              try:
                  input_box.send_keys(n1) 
                  print('正在申请中')
              except Exception as e:
                  print('fail')
              time.sleep(1) 

              input_box = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[7]/div/a/div[2]/div[2]/input")
              try:
                  input_box.send_keys(T1) 
              except Exception as e:
                  print('fail')
              time.sleep(1) 
                      
              #####################################################################################
              # 辅导员信息填写
              input_box = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[10]/div/a/div[2]/div[2]/input")
              try:
                  input_box.send_keys(n2)
                  print('正在申请中')
              except Exception as e:
                  print('fail')
              time.sleep(1) 

              input_box = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[11]/div/a/div[2]/div[2]/input")
              try:
                 input_box.send_keys(T2)
              except Exception as e:
                  print('fail')
              time.sleep(1) 
                          
              #####################################################################################
              # 请假类型
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(2) > div > a > span\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 选择因事出校（当天往返）
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(2) > div > div > div.mint-box-group > div > div > div > a:nth-child(1) > div.mint-cell-wrapper.mt-bColor-grey-lv5.mint-cell-no-bottom-line > div.mint-cell-title > label > span.mint-radiobox > span\").click();"
              browser.execute_script(js)
              time.sleep(1)
              
              #####################################################################################
              # 请假属性
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(3) > div > a > span\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 选择因公
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(3) > div > div > div.mint-box-group > div > div > div > a:nth-child(2) > div.mint-cell-wrapper.mt-bColor-grey-lv5.mint-cell-no-bottom-line > div.mint-cell-title > label > span.mint-radiobox > span\").click();"
              browser.execute_script(js)
              time.sleep(1)
              
              #####################################################################################
              # 因公类型
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(4) > div > a > span\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 选择实验
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(4) > div > div > div.mint-box-group > div > div > div > a:nth-child(3) > div.mint-cell-wrapper.mt-bColor-grey-lv5.mint-cell-no-bottom-line > div.mint-cell-title > label > span.mint-radiobox > span\").click();"
              browser.execute_script(js)
              time.sleep(1)        
              
              #####################################################################################
              # 通行开始时间
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > a \").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定年份
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(1) > ul > li:nth-child(" + str(int(tomorrow_year)-1919) + ")\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定月份
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(2) > ul > li:nth-child(" + tomorrow_month + ")\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定日期
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(3) > ul > li:nth-child(" + tomorrow_day + ")\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定小时 0
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(4) > ul > li:nth-child(1)\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定分钟 16
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(5) > ul > li:nth-child(17)\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 最后点确认
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(5) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__toolbar.mt-bColor-grey-lv6 > div.mint-picker__confirm.mt-color-theme\").click();"
              browser.execute_script(js)
              time.sleep(1)

              #####################################################################################
              # 通行结束时间
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > a\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定年份
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(1) > ul > li:nth-child(" + str(int(tomorrow_year)-1919) + ")\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定月份
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(2) > ul > li:nth-child(" + tomorrow_month + ")\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定日期
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(3) > ul > li:nth-child(" + tomorrow_day + ")\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定小时 23
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(4) > ul > li:nth-child(24)\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 确定分钟 52
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__columns > div:nth-child(5) > ul > li:nth-child(53)\").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 最后点确认
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(6) > div > div.mint-popup.mt-bg-white.mint-datetime.emapm-date-picker.mint-popup-bottom > div > div.mint-picker__toolbar.mt-bColor-grey-lv6 > div.mint-picker__confirm.mt-color-theme\").click();"
              browser.execute_script(js)
              time.sleep(1)

              #####################################################################################
              # 请假详情
              input_box = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[2]/div/div[2]/div[8]/div/a/div[2]/div[2]/div[1]/textarea")
              try:
                  input_box.send_keys(reas)
                  print('正在申请中')
              except Exception as e:
                  print('fail')
              time.sleep(1) 

              #####################################################################################
              # 活动校区
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(11) > div > a > span \").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 选择丁家桥校区
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(11) > div > div > div.mint-box-group > div > div > div > a:nth-child(3) > div.mint-cell-wrapper.mt-bColor-grey-lv5.mint-cell-no-bottom-line > div.mint-cell-title > div > label > span.mint-checkbox-new\").click();"
              browser.execute_script(js)
              time.sleep(1) 
              
              # 确定
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(11) > div > div > div.mint-selected-footer.__emapm > div.mint-selected-footer-bar > button.mint-button.mint-selected-footer-confirm.mt-btn-primary.mint-button--large\").click();"
              browser.execute_script(js)
              time.sleep(1) 
              
              #####################################################################################
              # 是否离开南京
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(12) > div > a \").click();"
              browser.execute_script(js)
              time.sleep(1)

              # 选择否
              js = "document.querySelector(\"#app > div > div > div > div.emapm-form > div:nth-child(2) > div > div.mint-cell-group-content.mint-hairline--top-bottom.mt-bg-white.mt-bColor-after-grey-lv5 > div:nth-child(12) > div > div > div.mint-box-group > div > div > div > a:nth-child(2) > div.mint-cell-wrapper.mt-bColor-grey-lv5.mint-cell-no-bottom-line > div.mint-cell-title > label\").click();"
              browser.execute_script(js)
              time.sleep(1) 

              #####################################################################################        
              # 地址
              input_box = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[2]/div/div[2]/div[20]/div/a/div[2]/div[2]/input")
              try:
                  input_box.send_keys(adres) 
                  print('正在申请中')
              except Exception as e:
                  print('fail')
              time.sleep(1) 

              #####################################################################################
              # 提交
              js = "document.querySelector(\"#app > div > div > div > div.mint-layout-container.sjakudbpe.OPjb4dozyy > button\").click();"
              browser.execute_script(js)
              print('出校审批已提交')
              time.sleep(5)
              
              #####################################################################################
              # log
              writeLog("已完成第二日出校审批")
              
              #####################################################################################
              # 检查是否通过                           
              checkpassed(browser)
              IFF()
         else:
              browser.close()
              print("------------网站出现故障，请稍候重试----------------")
              print("-------------------后台已关闭-----------------------")
              time.sleep(10)

if __name__ == "__main__":
    # user, pw, browser_loc = enterUserPW()
    userData = getUserData()
    loginData = json.loads(str(userData).strip())
    user = loginData['username']
    pw = loginData['password']
    n1 = loginData['name1']
    T1 = loginData['TN1']
    n2 = loginData['name2']
    T2 = loginData['TN2']
    reas = loginData['reason']
    adres = loginData['adress']
    browser_loc = loginData['loc']

    # 判断是否写入非默认安装位置的 Chrome 位置
    if len(browser_loc) > 10:
        chrome_options.binary_location = browser_loc    
    print(" ")
    print("Welcome to this Program which can Automatically Do THE F***ING DAILY JOB of Southeast University")
    print(" ")
    print("Copyrights belong to Everyone who Suffers this Hardship")
    print(" ")
    print("Version 1.6 by Someone named TimeLeSs or TimeLeSsROMO")
    print(" ")
    print("Tips：请确保在现版系统中进行过至少一次健康申报和出校审批，否则可能出现奇怪的错误导致无法正常运行")
    print("      各种问题可以联系TimeLeSs，如果你可以联系到我的话~_~")
    print(" ")
    qt1 = str(input("是否要进行健康申报，输入“Y”继续，输入“N”退出，输入“Z”则跳转至明日的出校审批: "))
    try:
         if qt1 == "N":
              print('本次运行结束，本窗口将在10秒后自动关闭，再见~')
              time.sleep(10)
              exit(0)
         elif qt1 == "Y":
              enterCampusRequist = True
              # 检查已过了健康申报时间
              if checkTime() == True:
                  print(' ')
                  print('注意，规定的今日健康申报最晚时间已过')
                  browser = webdriver.Chrome(
                  './chromedriver', options=chrome_options)
                  print("------------------已启动，后台运行中----------------------")
                  print("运行中，请稍候")
                  login(user, pw, browser)
                  browser.implicitly_wait(5)
                  dailyDone()
                  if dailyDone() is True:
                       print('恭喜，今日已进行过健康申报，如有问题可自行进入学校系统查看')
                  if dailyDone() is False:
                       print('今日未进行健康申报')
                  enterCampus(browser)
         
              else:
                  print(' ')
                  print('目前是健康申报的时间段，程序即将开始运行')

                  # 登录打卡一次试一试            
                  browser = webdriver.Chrome(
                  './chromedriver', options=chrome_options)
                  print("------------------已启动，后台运行中----------------------")
                  print("运行中，请稍候")
                  login(user, pw, browser)
                  browser.implicitly_wait(5)
                  time.sleep(5)

                  # 确认是否打卡成功            
                  if dailyDone() is True or dailyDone1 is True: # 今日已完成打卡
                      print('恭喜，今日已进行过健康申报，如有问题可自行进入学校系统查看')
                      time.sleep(2)

                      # 1.3 版本更新每日入校申请，自动申请第二日入校
                      if enterCampusRequist is True:
                          enterCampus(browser)
                          if checkEnterCampus(browser) is True: # 再确认一次，以免学校改版导致程序出错
                              print("即将检查出校审批是否通过")
                      checkpassed(browser)
                      IFF()

                  elif dailyDone() is False:  # 今日未完成打卡
                      print('开始今日健康申报')
                      # 点击报平安
                      buttons = browser.find_elements_by_css_selector('button')
                      for button in buttons:
                          if button.get_attribute("textContent").find("新增") >= 0:
                              button.click()
                              browser.implicitly_wait(5)

                              # 输入温度36.1-36.6°之间随机值
                              inputfileds = browser.find_elements_by_tag_name(
                                  'input')
                              for i in inputfileds:
                                  if i.get_attribute("placeholder").find("请输入当天晨检体温") >= 0:
                                      i.click()
                                      i.send_keys(str(random.randint(361, 366)/10.0))
                                     
                                      # 确认并提交
                                      buttons = browser.find_elements_by_tag_name(
                                          'button')
                                      for button in buttons:
                                          if button.get_attribute("textContent").find("确认并提交") >= 0:
                                              button.click()
                                              buttons = browser.find_elements_by_tag_name(
                                                  'button')
                                              button = buttons[-1]

                                              # 提交
                                              if button.get_attribute("textContent").find("确定") >= 0:
                                                  button.click()
                                                  dailyDone1 = True  # 标记已完成打卡
                                                  print('今日健康申报成功')
                                                  writeLog("今日健康申报成功")
                                                  time.sleep(2)
                                                  print('恭喜，今日已健康申报已完成，如有问题可自行进入学校系统查看')
                                              else:
                                                  print("WARNING: 学校可能改版，请及时更新脚本")
                                              break
                                      break
                              break
                      enterCampus(browser)
                      browser.quit()
                      print("-------------------后台已关闭----------------------")
                      print("本次运行结束，本窗口将在10秒后自动关闭，再见~")
                      time.sleep(10)
                      exit()
                  else:
                      browser.close()
                      print("------------网站出现故障，请稍候重试----------------")
                      print("-------------------后台已关闭-----------------------")
                      time.sleep(10)
         elif qt1 == "Z":
              browser = webdriver.Chrome(
               './chromedriver', options=chrome_options)
              print("------------------已启动，后台运行中----------------------")
              print("运行中，请稍候")
              login(user, pw, browser)
              browser.implicitly_wait(5)
              enterCampus(browser)
              browser.quit()
              print("-------------------后台已关闭----------------------")
              print("本次运行结束，本窗口将在10秒后自动关闭，再见~")
              time.sleep(10)
              exit()
    except:
         browser.close()
         print("------------网站出现故障，请稍候重试----------------")
         print("-------------------后台已关闭-----------------------")
         time.sleep(10)
