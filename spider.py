# -*-coding:utf-8-*-
import re
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import  PyQuery as pq
from config import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 创建数据库链接
client = MongoClient(MONGO_URL)
# 创建数据库
db = client[MONGO_DB]

browser = webdriver.PhantomJS(service_args=SEARVICE_ARGS)
browser.set_window_size(1400,800)
wait = WebDriverWait(browser, 10)

'''
1.设置页面搜索方法
'''

def search():
    print("正在搜索")
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
        '''
        UnicodeDecodeError: 'utf8' codec can't decode byte 0xe7
        in position 0: unexpected end of data
        '''
        # send_keys添加参数
        input.send_keys(KEYWORD)
        # 添加点击方法
        submit.click()

        # 监听翻页控件加载完,以显示"共xx页"显示完全为依据
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_product()
        return total.text
    except TimeoutException:
        print("超时")
        return search()

'''
2.设置自动翻页
'''
def get_next_page(page_number):
    print(u"正在翻页")
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
        get_product()
    except TimeoutException:
        print("get_next_page超时")
        get_next_page(page_number)

'''
3.解析页面，获取美食信息
'''
def get_product():
    print("正在获取产品")
    # 页面记载结束：主要是看商品信息的大节点是不是加载完了
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item"))
    )
    # 获取页面内容
    html = browser.page_source
    # 通过PyQuery解析页面
    doc = pq(html)
    # 根据节点获取美食的集合
    items = doc("#mainsrp-itemlist .items .item").items()
    # 遍历 获取各值
    for item in items:
        product = {
            # 获取img标签下的src属性
            "image": item.find(".pic .img").attr("src"),
            "price": item.find(".price").text(),
            "deal": item.find(".deal-cnt").text()[:-3],
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text()
        }
        save_to_mongo(product)

'''
4.存储数据
'''
def save_to_mongo(result):
    try:
        if db[MONGO_TAB].insert(result):
            print("正在存储到mongDB")
    except Exception:
        print("存储失败",result)
def main():
    try:
        totoal = search()
        pattern = re.compile(r"(\d+)")
        match = re.search(pattern, totoal)
        # 遍历获取所有的页面
        for i in range(2,int(match.group(1)) + 1):
            get_next_page(i)
        # 数据获取结束以后关闭浏览器
        # 如果用phantomJS。下面这句要注释不然报错
    except Exception:
        print("出错了")
    finally:
        browser.close()

if __name__ == "__main__":
    main()
