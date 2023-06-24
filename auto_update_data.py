from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
driver = webdriver.Chrome("./chromedriver.exe")

driver.get("https://im.tmu.edu.tw/")

account = "your_account"
password = "your_password"
time.sleep(1)

# 帳號
element = driver.find_element(by=By.XPATH,value="/html/body/div[2]/div/div[3]/div[3]/div[2]/div/div/div[1]/div/div/div[1]/div[3]/div/div/form/div[3]/div/input")
element.send_keys(account)

#密碼
element = driver.find_element(by=By.XPATH,value="/html/body/div[2]/div/div[3]/div[3]/div[2]/div/div/div[1]/div/div/div[1]/div[3]/div/div/form/div[4]/div/div[1]/input")
element.send_keys(password)

button = driver.find_element(by=By.XPATH,value="/html/body/div[2]/div/div[3]/div[3]/div[2]/div/div/div[1]/div/div/div[1]/div[3]/div/div/form/div[7]/div/button")
button.click()
time.sleep(2)

# 確認多用戶登入
try:
    button =driver.find_element(by=By.XPATH,value="/html/body/div[2]/div/div[3]/div[3]/div[2]/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[7]/div/div/div[2]/form/div[3]/div/a[1]/span")
    button.click()
except:
    pass

time.sleep(2)
# 15 pages
for page in range(1,4):
    driver.get(f"https://im.tmu.edu.tw/dashboard/latestDiscuss?type=&page={page}")
    
    time.sleep(1)
    
    all_discussion_lists = driver.find_element(by=By.CLASS_NAME, value="forum-tbody")
    discussion_list = all_discussion_lists.find_elements(by=By.CLASS_NAME, value="thread-toggle")

    # 點開那一頁的所有的標題
    for each in discussion_list:
        driver.execute_script('arguments[0].scrollIntoView();', each)
        each.click()
        time.sleep(0.5)

    title =all_discussion_lists.find_elements(by=By.CLASS_NAME, value="thread-container")
    reply_msgs = title[0].elements = driver.find_elements(By.CSS_SELECTOR, '.reply-box.clearfix')
    
    # 對每一個標題的留言操作
    for reply_msg in reply_msgs:
        
        # 知道目標標題的數量
        try:
            num = reply_msg.find_element(By.CSS_SELECTOR, '.fs-hint.pull-right').text
            num = int(num.split(" ")[0])
        except:
            continue
        

        gap = -10
        previous_reply_msgs = reply_msg.find_element(By.CSS_SELECTOR, '.btn-link.load-more-reply-btn')

        # 點開全部的留言
        try:
            for _ in range(num-1,0,gap):
                driver.execute_script('arguments[0].scrollIntoView();', previous_reply_msgs)
                previous_reply_msgs.click()
        except:
            pass
        time.sleep(2)

        all_btn = reply_msg.find_elements(by=By.CLASS_NAME, value="btn")
        # 如果還沒點過 就點
        for btn in all_btn:
            
            if btn.text == "+1":
                driver.execute_script('arguments[0].scrollIntoView();', btn)
                btn.click()
                time.sleep(0.2)
    time.sleep(1)
