#coding: utf-8
#from scrapy import cmdline

#cmdline.execute("scrapy crawl csdn --nolog".split())
import time
import os

while True:
    os.system("scrapy crawl csdn --nolog")
    os.system("scrapy crawl huanqiu --nolog")
    time.sleep(1800)  #每隔十分钟运行一次 3*10*60=1800s