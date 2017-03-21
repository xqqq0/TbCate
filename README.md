# TbCate


> * 
> * [selenium](http://selenium-python.readthedocs.io/waits.html)  [phantomJS](http://phantomjs.org)[PyQuery](https://pypi.python.org/pypi/pyquery)
[PythonPhantomJS](http://cuiqingcai.com/2577.html)
[PythonSelenium](http://cuiqingcai.com/2599.html)
[PythonPyQuery](http://cuiqingcai.com/2636.html)

# 
* 
* 
* PyQuary
* mongoDB 
* 

# 
*  selenium
`brew install selenium-server-standalone`
* PyQuery
  ` sudo easy_install pyquery`
* phantomjs
` brew install phantomjs`

#  selenium
> seleniumCSSid

### selenium
* 
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```
* 
`chromedriver`,Google[](http://www.jianshu.com/p/afd552124244)
![](http://upload-images.jianshu.io/upload_images/954728-18b0da24390f0d3a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![css](http://upload-images.jianshu.io/upload_images/954728-547988556270309f.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
# 
browser = webdriver.Chrome()
```


* 
```
wait = WebDriverWait(browser, 10)
```
* 
```
wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
``` 
* 
  * EC from selenium.webdriver.support import expected_conditions as EC
  * EC `EC`
  * By from selenium.webdriver.common.by import By
  * Byid css

* EC 
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

* By
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
### 
* ``EC`presence_of_element_located`cssid
* ``EC`element_to_be_clickable`css
* ```send_keys`
* ```click()`
* [](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains)
* send_keysPython2.7
`  UnicodeDecodeError: 'utf8' codec can't decode byte 0xe7in position 0: unexpected end of data`
` "".decode(encoding="utf-8")`
```
browser.get("https://s.taobao.com")
    # selenium
    # id
    # EC
    # csscss
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )

        # 
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > div > div.search-button > button"))
        )

        # seleniumAPI
        # send_keys
        input.send_keys(KEYWORD)
        # 
        submit.click()
```
### 
* ,`xx`
* EC`presence_of_element_located`css

* 
```
 total = wait.until(
       EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
  )
return total.text
```
### 
> 
  * 
  * 
![](http://upload-images.jianshu.io/upload_images/954728-4483a276f47d8342.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 
* 
* 

``` 
def get_next_page(page_number):
    print(u"")
    try:
    #   
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.form > input"))
        )

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()

        # 
        text = wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number))
        )
        get_product()
    except TimeoutException:
        print("get_next_page")
        get_next_page(page_number)
```

# PyQuery
> PyQuery(pq)jQueryidcss`id``mainsrp-itemlist``css``items``css``items`,
![](http://upload-images.jianshu.io/upload_images/954728-f594e45ac4a6a326.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 
```
'''
3.
'''
def get_product():
    print("")
    # 
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item"))
    )
    # 
    html = browser.page_source
    # PyQuery
    doc = pq(html)
    # 
    items = doc("#mainsrp-itemlist .items .item").items()
    #  
    for item in items:
        product = {
            # imgsrc
            "image": item.find(".pic .img").attr("src"),
            "price": item.find(".price").text(),
            "deal": item.find(".deal-cnt").text()[:-3],
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text()
        }
```

* 
 * 

# mongoDB
> mongoDB

* 
```
MONGO_URL = "localhost"
MONGO_DB = "Taobao"
MONGO_TAB = "TbCate"
```

* 
```
# 
client = MongoClient(MONGO_URL)
# 
db = client[MONGO_DB]
```
* 
```
'''
4.
'''
def save_to_mongo(result):
    try:
        if db[MONGO_TAB].insert(result):
            print("mongDB")
    except Exception:
        print("",result)
```

# 
```
def main():
    try:
        # 
        totoal = search()
        # 
        pattern = re.compile(r"(\d+)")
        match = re.search(pattern, totoal)
        # 
        for i in range(2,int(match.group(1)) + 1):
            get_next_page(i)
        # 
    except Exception:
        print("")
   # 
    finally:
        browser.close()
```

# phantomJS
> phantomJS

* phantomJS
 ```
# GooglePhantomJS
browser = webdriver.PhantomJS()
# 
browser.set_window_size(1400,800)
```

* PhantomJS[](http://phantomjs.org/api/command-line.html)
  * 
```
# phantomJS
SEARVICE_ARGS = ["--load-images=false","--disk-cache=true"]
```
  * 
```
browser = webdriver.PhantomJS(service_args=SEARVICE_ARGS)
```

# 
* `selenium` 
*  `PhantomJS`browser.close()finally
* mongoDBmong
* `PyQuery``PhantomJS`GitHubREADME
* [](https://github.com/xqqq0/TbCate)