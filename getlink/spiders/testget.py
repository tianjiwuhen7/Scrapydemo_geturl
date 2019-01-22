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
class csdnSpider(Spider):
    name="csdn"
    #download_delay=1

    #allowed_domains=["ent.qq"]
    start_urls=[
        "http://ent.qq.com/"
    ]
    custom_settings = {
     'ITEM_PIPELINES':{
         'getlink.pipelines.GetlinkPipeline': 300,
     }
 }

    #start_urls=hehe.deal_url()
#    def parsess(self,response):
#        sel=Selector(response)
#        item=GetlinkItem()
#        title=sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()
#        article_url = str(response.url)
#        time=sel.xpath('//div[@id="article_details"]/div[2]/div/span[@class="link_postdate"]/text()').extract()
#        readtimes=sel.xpath('//div[@id="article_details"]/div[2]/div/span[@class="link_view"]/text()').extract()
#        item['title']=[n.encode('utf-8').replace("\r\n","").strip() for n in title]
#        print item['title']
#        item['time']=[n.encode('utf-8') for n in time]
#        item['readtimes']=[n.encode('utf-8') for n in readtimes]
#        yield item
#        #get next url
#        urls=sel.xpath('//li[@class="next_article"]/a/@href').extract()
#        for url in urls:
#            print url
#            url="http://blog.csdn.net"+url
#            print url
#            yield Request(url,callback=self.parse)
    def parse2(self, response):
        hxs = Selector(response)
        #item = GetlinkItem()
        item = response.meta['item']
        item['url'] = response.url
        #item['title'] = hxs.xpath('//div[@class="hd"]/h1/text()').extract()
        s_title=hxs.xpath('//div[@class="hd"]/h1/text()').extract()
        s_content=hxs.xpath('//div[@class="Cnt-Main-Article-QQ"]//p/text()').extract()
        s_pubTime=hxs.xpath('//div[@class="a_Info"]/span[@class="a_time"]/text()').extract()
        s_author = hxs.xpath('//div[@class="qq_editor"]/text()').extract()
        item['title']=' '.join(s_title)
        item['type'] ="News"
        item['source'] ="腾讯娱乐"
        item['content'] =' '.join(s_content)
        item['saveTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if s_pubTime:
            item['pubTime'] = ' '.join(s_pubTime) + ":00"
        else:
            pass
        #item['pubTime'] = ' '.join(s_pubTime)+":00"
        item['site'] = "腾讯娱乐"
        item['author'] = ' '.join(s_author)
        print ' '.join(item['title'])
        print ' '.join(item['saveTime'])
        print response.url
        return item
    def parse(self,response):
        hxs = Selector(response)
        #hxs = HtmlXPathSelector("http://ent.qq.com/")
        sites = hxs.xpath('//div[@class="Q-tpList"]//em/a')
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
    def parse3(self, response):
        soup = BeautifulSoup(response.body)
        print response.url
        tag = soup.find("div", attrs={"class":"Cnt-Main-Article-QQ", "id":"Cnt-Main-Article-QQ"}) # 提取第一个标签
        content_list = [tag_i.text for tag_i in tag.findAll("p")]
        content = "".join(content_list)
        print "nihaocontent"
        # item = WechatprojectItem() ## 只抓取二级页面数据
        item = response.meta['item'] ## 抓取当前页数和二级页面数据
        item["title"] = "sucess"
        item["link"] = response.url
        item["desc"] =content
        #print str(item['title'].encode("utf8"))
        #print str(item["link"].encode("utf8"))
        #print str(item["desc"].encode("utf8"))
        return item
