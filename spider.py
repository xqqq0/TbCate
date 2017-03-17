# -*-coding:utf-8-*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
'''
1.设置页面搜索方法
'''


def search():
    browser.get("https://wwww.taobao.com")
    # selenium处理页面等待的方法
    # 设置一下需要监听的元素，可以通过id或者能唯一确定元素的属性
    # EC是选择条件点后边的是条件，我把条件记录在简书里

    try:
        # 我们通过页面元素，查找到输入框，我们利用css样式去确定，并利用css选择器去获取
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )

        # 然后监听按钮，条件是以可以点击判断其加载完成
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > button"))
        )
    finally:
        browser.quit()

