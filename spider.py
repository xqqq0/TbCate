# -*-coding:utf-8-*-
from selenium import webdriver
import time

dr = webdriver.Chrome()

time.sleep(5)

print 'Browser will be closed'

dr.quit()

print 'Browser is close'