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
    browser.get("https://s.taobao.com")
    # selenium处理页面等待的方法
    # 设置一下需要监听的元素，可以通过id或者能唯一确定元素的属性
    # EC是选择条件点后边的是条件，我把条件记录在简书里

    # 我们通过页面元素，查找到输入框，我们利用css样式去确定，并利用css选择器去获取
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
    )

    # 然后监听按钮，条件是以可以点击判断其加载完成
    # #J_SearchForm > div > div.search-button > button
    # J_SearchForm > div > div.search-button > button
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > div > div.search-button > button"))
    )

    # 调用selenium的API来给搜索框输入内容，然后按钮追加点击方法
    keyword = "美食".decode(encoding="utf-8")
    input.send_keys(keyword)
    submit.click()

def main():
    search()

if __name__ == "__main__":
    main()
