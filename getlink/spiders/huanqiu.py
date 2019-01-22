#coding: utf-8
import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from getlink.items import GetlinkItem
import time
import datetime
import logging
class huanqiuSpider(Spider):
    name="huanqiu"
    #download_delay=1

    #allowed_domains=["ent.qq"]
    start_urls=[
        "http://china.huanqiu.com/leaders/",
        "http://world.huanqiu.com/exclusive/",
        "http://china.huanqiu.com/local/",
        "http://china.huanqiu.com/leaders/",
        "http://oversea.huanqiu.com/article/",
        "http://society.huanqiu.com/socialnews/",
        "http://ent.huanqiu.com/article/",
        "http://taiwan.huanqiu.com/article/",
        "http://mil.huanqiu.com/china/",
        "http://mil.huanqiu.com/world/",
        "http://mil.huanqiu.com/observation/",
        "http://women.huanqiu.com/beauty/",
        "http://fashion.huanqiu.com/pic/",
        "http://women.huanqiu.com/xzml/",
        "http://tech.huanqiu.com/front/",
        "http://tech.huanqiu.com/superplayer/",
        "http://world.huanqiu.com/regions/",
        "http://finance.huanqiu.com/chanjing/",
        "http://finance.huanqiu.com/caigc/",
        "http://finance.huanqiu.com/jinr/",
        "http://finance.huanqiu.com/lingdu/",
        "http://finance.huanqiu.com/gjcx/",
        "http://ent.huanqiu.com/star/mingxing-neidi/",
        "http://sports.huanqiu.com/soccer/gn/",
        "http://health.huanqiu.com/health_news/",
        "http://history.huanqiu.com/china/"
    ]
    custom_settings = {
     'ITEM_PIPELINES':{
         'getlink.pipelines.GetlinkPipeline': 300,
     }
 }
    def parse2(self, response):
        hxs = Selector(response)
        #item = GetlinkItem()
        item = response.meta['item']
        item['url'] = response.url
        #item['title'] = hxs.xpath('//div[@class="hd"]/h1/text()').extract()
        s_title=hxs.xpath('//div[@class="conText"]/h1/text()').extract()
        s_content=hxs.xpath('//div[@id="text"]/p/text()').extract()
        s_pubTime=hxs.xpath('//div[@class="summaryNew"]/strong[@class="timeSummary"]/text()').extract()
        s_author = hxs.xpath('//div[@class="editorSign"]/span[@id="editor_baidu"]/text()').extract()
        item['title']=' '.join(s_title)
        item['type'] ="News"
        item['source'] ="环球网"
        item['content'] =' '.join(s_content)
        item['saveTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if s_pubTime:
            item['pubTime'] = ' '.join(s_pubTime)
        else:
            pass
        #item['pubTime'] = ' '.join(s_pubTime)+":00"
        item['site'] = "环球网"
        item['author'] = ' '.join(s_author)
        print ' '.join(item['title'])
        #print s_content
        print ' '.join(item['saveTime'])
        print response.url
        return item
    def parse(self,response):
        hxs = Selector(response)
        #hxs = HtmlXPathSelector("http://ent.qq.com/")
        sites = hxs.xpath('//div[@class="fallsFlow"]//li/h3/a')
        for site in sites:
            item=GetlinkItem()
            #item['title'] = site.select('a/text()').extract()
            item['link'] = site.xpath("@href").extract()
            #print "diyibu"
            #print item['link']
            #item['desc'] = site.select('a/text()').extract()
            next_url = item["link"][0]
            # yield Request(url=next_url, callback=self.parse2) ## 只抓取二级页面数据
            yield Request(url=next_url, meta={"item":item}, callback=self.parse2) ## 抓取当前页数和二级页面数据