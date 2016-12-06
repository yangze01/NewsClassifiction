#coding=utf-8
from bs4 import BeautifulSoup
from newsOnMysql import *
from NewsUnit import *
import requests
import datetime
import html5lib
import time
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
TIMESTAMP = time.strftime('%Y%m%d')
def get_today_list():
    valid_timestamp_url_list=list()
    valid_item_list = list()
    url_pattern = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=%s&r=0.30903104213777677'
    start_page_num = 1
    for page_num in range(start_page_num,start_page_num+2):
        print(page_num)
        url = url_pattern%page_num
        try:
            res = requests.get(url,timeout = 10)
            html = res.content.decode('gbk').encode('utf8')
            # print(html)
        except BaseException:
            print("timed out in page url:%s"%url)
        try:

            page_url_list = re.findall(r'url : "(http://.*)",type', html)
            page_item_list = re.findall(r'channel : {title : "(.*)",id',html)

            url_list_timestamp = page_url_list[-1].split('/')[-2].replace('-', '')
            print(url_list_timestamp)
        except BaseException:
            print("div not pattern in page_url: %s"%url)
            continue
        if url_list_timestamp != TIMESTAMP:
            print(url_list_timestamp)

            for url in page_url_list:
                url_list_timestamp = url.split('/')[-2].replace('-','')
                if url_list_timestamp ==  TIMESTAMP:
                    print("-------stored---------",url_list_timestamp,"-----------------------")
                    valid_timestamp_url_list.append(url)
                    valid_item_list.append(page_item_list[page_url_list.index(url)])

        else:
            print("-------stored---all---page---------")
            valid_timestamp_url_list = valid_timestamp_url_list + page_url_list
            valid_item_list = valid_item_list + page_item_list
        # for i in valid_timestamp_url_list:
        #     print i
    return zip(valid_item_list,valid_timestamp_url_list)

class Begin_crawler(object):
    def __init__(self):
        self.user_unit = NewsUnit().news_unit
        self.opt_news_mysql = NewsOnMysql()

    

    def read_url_list(self,urltuple_list):
        try:
            for urltuple in urltuple_list:
                self.news_unit = read_url_list(urltuple)
                self.opt_news_mysql.insertOneNews(self.news_unit)
        except:

            print("div not pattern in page_url:%s"%urltuple[1])
        else:
            print("OK!")

    def read_one_news(self,urltuple):
        news_tmp = dict()
        category = urltuple[0]
        url = urltuple[1]
        news_id = url.split('/')[-1]
        print(news_id)
        print("________+_________+_________")
        res = requests.get(urltuple[1],timeout = 10)
        print(category)
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')
        time =  url.split('/')[-2].replace('-','')
        print(time)
        title = soup.find('title').text.split(' ')[0]
        print(title)
        div_lelvel_str = soup.find('div', id='artibody')
        p_level_list = div_lelvel_str.find_all('p')
        content_real = ''
        for item in p_level_list:
            content_real = content_real + item.text.strip()
        print(content_real)
        news_tmp["_id"] = news_id
        news_tmp["title"] = title
        news_tmp["content"] = content
        news_tmp["time"] = time
        news_tmp["category"] = category
        return news_tmp


if __name__ == "__main__":


    url = ("1","http://finance.sina.com.cn/roll/2016-12-02/doc-ifxyhwyy0427396.shtml")
    # url1 = "http://mil.news.sina.com.cn/china/2016-12-04/doc-ifxyiayq2241339.shtml"
    # url2 = "http://video.sina.com.cn/p/news/w/doc/2016-12-04/224165432533.html"
    # url3 = "http://sports.sina.com.cn/cba/2016-12-05/doc-ifxyiayq2332232.shtml"

    testuser = Begin_crawler()
    testuser.read_one_news(url)
