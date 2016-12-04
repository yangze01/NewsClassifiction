#coding=utf-8
from bs4 import BeautifulSoup
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
    url_pattern = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=%s&r=0.30903104213777677'
    start_page_num = 1
    for page_num in range(start_page_num,start_page_num+30,3):
        print(page_num)
        url = url_pattern%page_num
        try:
            res = requests.get(url,timeout = 10)
            html = res.text.encode('ISO-8859-1')##.#encode('UTF-8')#.encode('UTF-8')#
        except BaseException:
            print("timed out in page url:%s"%url)
        try:
            page_url_list = re.findall(r'url : "(http://.*\.shtml)"', html)
            url_list_timestamp = page_url_list[-1].split('/')[-2].replace('-', '')
        except BaseException:
            print("div not pattern in page_url:"%url)
            continue
        if url_list_timestamp != TIMESTAMP:
            print(url_list_timestamp)

            for url in page_url_list:
                url_list_timestamp = url.split('/')[-2].replace('-','')
                # print("---------unstored---------",url_list_timestamp,"--------------------")
                if url_list_timestamp ==  TIMESTAMP:
                    print("-------stored---------",url_list_timestamp,"-----------------------")
                    valid_timestamp_url_list.append(url)
        else:
            print("-------stored---all---page---------")
            valid_timestamp_url_list = valid_timestamp_url_list + page_url_list
    return valid_timestamp_url_list


def read_news(url):
    res = requests.get(url,timeout = 10)



if __name__ == "__main__":
    item_url_info_list = list()
    # url = "http://finance.sina.com.cn/roll/2016-12-02/doc-ifxyhwyy0427396.shtml"
    url1 = "http://mil.news.sina.com.cn/china/2016-12-04/doc-ifxyiayq2241339.shtml"
    res = requests.get(url1,timeout = 10)
    content = res.content
    print(content)
    soup = BeautifulSoup(content, 'html5lib')
    title = soup.find('h1', id='artibodyTitle').text.strip()
    # title = soup.find('h1', id='main_title').text.strip()
    # print(title)
    # item_url_info_list.append(title)
    # div_lelvel_str = soup.find('div', id='artibody')
    # p_level_list = div_lelvel_str.find_all('p')

    # content_list = [item.text.strip()+'\n' for item in p_level_list]
    # print("----------------------------")
    # print(content_list[1])
    # item_url_info_list.extend(content_list)
    # print("----------------------------")
    # print(item_url_info_list[2])
