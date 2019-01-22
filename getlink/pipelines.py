# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
#import logging
import sys
reload(sys)
from scrapy.conf import settings
import MySQLdb
sys.setdefaultencoding('utf8')
class GetlinkPipeline(object):
    def process_item(self, item, spider):
        #logging.Error("runing here")
        today = time.strftime('%Y%m%d',time.localtime())
        fileName = today + 'movie.txt'
        with open(fileName,'a') as fp:
            fp.write(str(item['url'].encode("utf8")) + '\t' + str(item['title'].encode("utf8"))+ '\t' + (item['content'].encode("utf8"))+'\t' + str(item['type'].encode("utf8"))+'\t' + str(item['source'].encode("utf8"))+'\t' + str(item['saveTime'].encode("utf8"))+'\t' + str(item['pubTime'].encode("utf8"))+'\t' + str(item['site'].encode("utf8"))+'\t' + str(item['author'].encode("utf8"))+ '\n')
        return item
    def process_item1(self, item, spider):
        print "run process_item"
        # DBKWARGS=spider.settings.get('DBKWARGS')
        # con=MySQLdb.connect(**DBKWARGS)
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']
        con = MySQLdb.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        cur = con.cursor()
        sql = ("insert into tb_mdsd_080(url, title, content, type,source,saveTime,pubTime,site,author ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # sql=("insert into testweibo values(?,?,?,?,?,?)")
        list = [str(item['url'].encode("utf8")),
                str(item['title'].encode("utf8")),
                str(item['content'].encode("utf8")),
                str(item['type'].encode("utf8")),
                str(item['source'].encode("utf8")),
                str(item['saveTime'].encode("utf8")),
                str(item['pubTime'].encode("utf8")),
                str(item['site'].encode("utf8")),
                str(item['author'].encode("utf8"))]
        try:
            print "start insert"
            cur.execute(sql, list)
        except Exception, e:
            print('Insert error', e)
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item
