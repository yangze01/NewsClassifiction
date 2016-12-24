#coding=utf-8
from bs4 import BeautifulSoup
import requests
import datetime
import html5lib
import time
import os
import re
import sys
import threading
import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')
TIMESTAMP = "20161202"
# TIMESTAMP = time.strftime('%Y%m%d')
# def page_list():
TIMESTAMP = time.strftime('%Y%m%d')
def get_page_list(start_page_num,end_page_num):
    valid_timestamp_url_list=list()
    valid_item_list = list()
    url_pattern = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=%s&r=0.30903104213777677'
    # start_page_num = 0
    for page_num in range(start_page_num,end_page_num):
        print(page_num)
        url = url_pattern%page_num
        try:
            res = requests.get(url,timeout = 10)
            html = res.content.decode('gbk').encode('utf8')

        except BaseException:
            print("timed out in page url:%s"%url)
        try:

            # pattern1 = r'url : "(http://.*)",type'
            # pattern2 = r'channel : {title : "(.*)",id'

            pattern1 = r'channel : {title : "(.*)",id.*?url : "http://.*\.shtml",type'
            pattern2 = r'channel : {title : ".*",id.*?url : "(http://.*\.shtml)",type'
            page_item_list = re.findall(pattern1,html)
            page_url_list = re.findall(pattern2,html)
            print("page_item_list len"+str(len(page_item_list)))
            print("page_url_list len"+str(len(page_url_list)))
            url_list_timestamp = page_url_list[-1].split('/')[-2].replace('-', '')
            print(url_list_timestamp)
        except BaseException:
            print("div not pattern in page_url: %s"%url)
            continue

        print("-------stored---all---page---------")
        valid_timestamp_url_list = valid_timestamp_url_list + page_url_list
        valid_item_list = valid_item_list + page_item_list

    return zip(valid_item_list,valid_timestamp_url_list)

def get_today_list():
    TIMESTAMP = time.strftime('%Y%m%d')
    valid_timestamp_url_list=list()
    valid_item_list = list()
    url_pattern = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=%s&r=0.30903104213777677'
    start_page_num = 45
    for page_num in range(start_page_num,start_page_num+50):
        print(page_num)
        url = url_pattern%page_num
        try:
            res = requests.get(url,timeout = 10)
            html = res.content.decode('gbk').encode('utf8')
            # print(html)
        except BaseException:
            print("timed out in page url:%s"%url)
        try:

            # pattern1 = r'url : "(http://.*)",type'
            # pattern2 = r'channel : {title : "(.*)",id'

            pattern1 = r'channel : {title : "(.*)",id.*?url : "http://.*\.shtml",type'
            pattern2 = r'channel : {title : ".*",id.*?url : "(http://.*\.shtml)",type'
            page_item_list = re.findall(pattern1,html)
            page_url_list = re.findall(pattern2,html)
            print("page_item_list len"+str(len(page_item_list)))
            print("page_url_list len"+str(len(page_url_list)))
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

    return zip(valid_item_list,valid_timestamp_url_list)
