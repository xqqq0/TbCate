# -*-coding:utf-8-*-
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

    try:
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
        # send_keys添加参数
        input.send_keys(keyword)
        # 添加点击方法
        submit.click()

        # 监听翻页控件加载完,以显示"共xx页"显示完全为依据
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )

        return total.text

    except TimeoutException:
        print("超时")
        return search()

def get_next_page(page_number):
    try:
    # 拿到输入框 和确定 按钮，然后输入页码
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.form > input"))
        )

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()

        # 翻页后确定当前面是否加载完，主要看页码当时是否为高亮状态
        text = wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number))
        )
    except TimeoutException:
        print("get_next_page超时")
        get_next_page(page_number)

def main():
    totoal = search()
    pattern = re.compile(r"(\d+)")
    match = re.search(pattern, totoal)
    # 遍历获取所有的页面
    for i in range(2,int(match.group(1)) + 1):
        get_next_page(i)
    # if match:
    #     print  match.group(1)
    # else:
    #     print("页面匹配失败")

if __name__ == "__main__":
    main()
