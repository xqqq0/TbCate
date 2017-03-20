# -*-coding:utf-8 -*-
# mongodb的配置
MONGO_URL = "localhost"
MONGO_DB = "Taobao"
MONGO_TAB = "TbCate"

# phantomJS的高级用配置：不加载图片，加缓存
SEARVICE_ARGS = ["--load-images=false","--disk-cache=true"]

KEYWORD = "美食".decode(encoding="utf-8")