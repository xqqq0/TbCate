> * 本文是我接触爬虫以来，第三套爬虫的代码记录博客。
> * 本文主要是记录淘宝搜索美食的页面信息，工具是[selenium](http://selenium-python.readthedocs.io/waits.html) 和 [phantomJS](http://phantomjs.org)，框架[PyQuery](https://pypi.python.org/pypi/pyquery)其实对于以上框架或者工具，仅仅停留在使用的初级阶段，具体可以参看崔老师的相关博客：
[Python爬虫利器四之PhantomJS的用法](http://cuiqingcai.com/2577.html)
[Python爬虫利器五之Selenium的用法](http://cuiqingcai.com/2599.html)
[Python爬虫利器六之PyQuery的用法](http://cuiqingcai.com/2636.html)

# 思路
* 模拟在淘宝的搜索框填写关键词，然后搜索
* 模拟数据加载完毕后，点击下一页操作
* 数据加载结束以后利用PyQuary进行数据解析提取
* 存储到mongoDB
* 代码细节优化

# 工具安装
* 安装 selenium
`brew install selenium-server-standalone`
* 安装PyQuery
  ` sudo easy_install pyquery`
* 安装phantomjs
` brew install phantomjs` 

# 利用 selenium模拟淘宝操作
> 使用selenium的大致思路根据CSS选择器或者id之类的定位到具体的控件，然后给控件实现赋值或者点击等操作。

### selenium的简单配置
* 导入框架
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```
* 加载浏览器驱动，本例中使用谷歌浏览器，使用前请确认已经安装
`chromedriver`,关于配置可以自行Google或者访问我的[博客](http://www.jianshu.com/p/afd552124244)
![支持的浏览器](http://upload-images.jianshu.io/upload_images/954728-18b0da24390f0d3a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![选择元素css](http://upload-images.jianshu.io/upload_images/954728-547988556270309f.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
# 加载驱动
browser = webdriver.Chrome()
```
此时代码运行可以呼起一个空置的谷歌浏览器

* 设置等待超时时间：在规定时间内未能加载相应控件将报错
```
wait = WebDriverWait(browser, 10)
```
* 通用写法
```
wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
``` 
* 代码分析
  * EC 为from selenium.webdriver.support import expected_conditions as EC
  * EC后边的是选择条件，即什么时候可以选择控件，例中条件为控件完全展示，其他选择条件请看下面 `EC选择条件`
  * By 为from selenium.webdriver.common.by import By
  * By后边的是根据什么元素选择控件，可以使id 或者css等等，后边的参数为具体的元素值

* EC选择条件 
```
title_is
title_contains
presence_of_element_located
visibility_of_element_located
visibility_of
presence_of_all_elements_located
text_to_be_present_in_element
text_to_be_present_in_element_value
frame_to_be_available_and_switch_to_it
invisibility_of_element_located
element_to_be_clickable
staleness_of
element_to_be_selected
element_located_to_be_selected
element_selection_state_to_be
element_located_selection_state_to_be
alert_is_present
```

* By参数类型
```
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
```
### 模拟关键字填写及搜索
* `输入框`的EC条件为`presence_of_element_located`，然后利用其css选择器，并复制其id
* `确定按钮`EC条件为`element_to_be_clickable`同样选择其css值
* `输入框`内通过`send_keys`传入搜索词
* `确定按钮`调用`click()`方法
* 其他的方法参见[文档](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains)
* 坑：send_keys输入关键字的时候，在Python2.7的环境中，如果直接用字符串会报错
`  UnicodeDecodeError: 'utf8' codec can't decode byte 0xe7in position 0: unexpected end of data`
可以通过解码进行修复` "美食".decode(encoding="utf-8")`
```
browser.get("https://s.taobao.com")
    # selenium处理页面等待的方法
    # 设置一下需要监听的元素，可以通过id或者能唯一确定元素的属性
    # EC是选择条件点后边的是条件，我把条件记录在简书里
    # 我们通过页面元素，查找到输入框，我们利用css样式去确定，并利用css选择器去获取
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )

        # 然后监听按钮，条件是以可以点击判断其加载完成
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > div > div.search-button > button"))
        )

        # 调用selenium的API来给搜索框输入内容，然后按钮追加点击方法
        # send_keys添加参数
        input.send_keys(KEYWORD)
        # 添加点击方法
        submit.click()
```
### 获取宝贝页面的宝贝总页数
* 监听翻页控件加载完,以显示`共xx页`显示完全为依据
* EC的条件也就是`presence_of_element_located`，同样利用其css选
择器
* 将返回页数作为返回值返回
```
 total = wait.until(
       EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
  )
return total.text
```
### 实现翻页
> 翻页功能有种实现方式
  * 点击下一页，实现翻页，但是如果发生错误不易差别是具体页数
  * 输入页码，点击确定，可以清楚的知道具体跳转了那一页，翻页后确定当前面是否加载完，主要看页码当时是否为高亮状态
![](http://upload-images.jianshu.io/upload_images/954728-4483a276f47d8342.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 定义一个以页码作为参数的函数
* 获取页码户输入框架，获取确定按钮，输入框填入参数，然后点击确定实现翻页，与搜索功能相同
* 确定当前页码的高亮状态来

``` 
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
```

# PyQuery实现页面解析
> 对于PyQuery(以下简称pq)的用法目前完全懵逼，完全是跟着视频敲的，只知道类似于jQuery，根据id或者css样式去获取查找元素，页面结果见下图，通过`id`为`mainsrp-itemlist`的，然后`css`样式为`items`获取商品列表，最后通过`css`样式为`items`,然后每个商品的信息
![网页结构图](http://upload-images.jianshu.io/upload_images/954728-f594e45ac4a6a326.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 没啥说的直接上代码
```
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
```

* 在第一次加载页面方法时，也就是第一页的时候调用此方法，获取第一页的数据
 * 在翻页的时候也要调用此方法

# 存储到mongoDB
> 与第一篇爬取头条数据一样，需要单独创建配置文件，然后创建俩呢及，创建数据库，存储数据，有一点着重提示的是，在代码运行存储数据的时候，一定要记得开启mongoDB的服务，不然会报一些莫名其妙的错误

* 配置文件代码
```
MONGO_URL = "localhost"
MONGO_DB = "Taobao"
MONGO_TAB = "TbCate"
```

* 创建数据库连接
```
# 创建数据库链接
client = MongoClient(MONGO_URL)
# 创建数据库
db = client[MONGO_DB]
```
* 存储数据
```
'''
4.存储数据
'''
def save_to_mongo(result):
    try:
        if db[MONGO_TAB].insert(result):
            print("正在存储到mongDB")
    except Exception:
        print("存储失败",result)
```

# 代码整体串接
```
def main():
    try:
        # 获取总页数
        totoal = search()
        # 获取数字，过滤汉字
        pattern = re.compile(r"(\d+)")
        match = re.search(pattern, totoal)
        # 遍历获取所有的页面
        for i in range(2,int(match.group(1)) + 1):
            get_next_page(i)
        # 数据获取结束以后关闭浏览器
    except Exception:
        print("出错了")
   # 用完后，必须关闭浏览器
    finally:
        browser.close()
```

# 引入phantomJS
> 我感觉如果遇到一个具体类似淘宝宝贝数据爬取的需求的话，可能的大致思路是先通过浏览器去模拟数据，成功以后，引入phantomJS去静默爬取数据

* 配置phantomJS
 ```
# 将Google浏览器换成PhantomJS
browser = webdriver.PhantomJS()
# 修改弹框大小
browser.set_window_size(1400,800)
```

* PhantomJS的一些高级配置，详见[官网](http://phantomjs.org/api/command-line.html)
  * 在配置文件中简单进行配置
```
# phantomJS的高级用配置：不加载图片，加缓存
SEARVICE_ARGS = ["--load-images=false","--disk-cache=true"]
```
  * 代码中引入
```
browser = webdriver.PhantomJS(service_args=SEARVICE_ARGS)
```

# 一些注意点
* `selenium` 等待控件加载的时候，容易发生超时问题，所以要加异常处理，一般超时后都是在调用一遍方法
* 引入 `PhantomJS`以后，browser.close()会报错，所以也要加异常处理，在finally后边关闭
* 存储到mongoDB的时候一定要先开启mong服务
* 本博客对`PyQuery`和`PhantomJS`没有进行详细的讲解，因为本人基础薄弱，但是给了一些博客链接，待到本人学习以后会将博客进行完善，另外本博客在GitHub的源码README中同步更新了
* [代码地址](https://github.com/xqqq0/TbCate)