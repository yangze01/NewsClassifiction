#coding=utf-8
from bs4 import BeautifulSoup
from optOnMysql.NewsOnMysql import *
from optOnMysql.NewsUnit import *
from writeRead.WriteRead import *
from writeRead.NewsJson import *
import requests
import datetime
import html5lib
import time
import os
import re
import sys
import threading
import os

reload(sys)
sys.setdefaultencoding('utf8')

# TIMESTAMP = time.strftime('%Y%m%d')
TIMESTAMP = "20161202"
# def page_list():
# TIMESTAMP = time.strftime('%Y%m%d')
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

class Begin_crawler(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self)
        self.news_unit = NewsUnit().news_unit
        self.opt_news_mysql = NewsOnMysql()
        self.threadname = threadname
        self.news_id = ''
        self.catch_tuple = list()
        # self.news
        self.opt_file = NewsJson('queue.json','visited.json')
        # self.opt_queue_file = Write_Read('queue.json')
        # self.opt_visited_file = Write_Read('visited.json')
    def run(self):
        global queue
        global visited
        i = 1
        try:
            while queue:
                print("++++++++++++++++++1+++++++++++++++++++++")
                if queue:
                    CONDITION.acquire()
                    self.catch_tuple = queue.pop()
                    CONDITION.release()
                    news_id = self.catch_tuple[1].split('/')[-1]
                    print(news_id)
                    # print(catch_tuple)
                    print(self.threadname+": the url will be read:"+self.catch_tuple[1])
                    if news_id not in visited:
                        visited |= {news_id}
                        print("before read_one_news")
                        print("++++++++++++++++++2+++++++++++++++++++++")
                        self.news_unit = self.read_one_news(self.catch_tuple)
                        print("before insert")
                        # print(self.news_unit["content"])
                        # print(self.news_unit["title"])
                        # print(self.news_unit["category"])
                        self.opt_news_mysql.insertOneNews(self.news_unit)
                        print("the queue len is "+str(len(queue)))
                    i = i+1
                    print("the visited len is: "+ str(len(visited)))
            self.opt_file.save_queue(queue)
            self.opt_file.save_visited(list(visited))
        except:
            # queue = queue.append(catch_tuple)
            print("except")
            print(self.catch_tuple[0])
            print(self.catch_tuple[1])
            self.opt_file.save_queue(queue)
            self.opt_file.save_visited(list(visited))
        else:
            print("Ok")

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
        print("++++++++++++++++++3+++++++++++++++++++++")
        news_tmp = dict()
        category = urltuple[0]
        url = urltuple[1]
        news_id = url.split('/')[-1]
        # print(news_id)
        print("________+_________+_________")
        print(urltuple[1])
        try:
            res = requests.get(urltuple[1],timeout = 50)
            print("++++++++++++++++++4+++++++++++++++++++++")
            time.sleep(random.randint(2,10))
            # print(res.content)
        except:
            # print(res.content)
            print("e")
        print("===========================category==============================")
        print(category)
        content = res.content
        ####################################################################

        ###############################################################
        print("before using soup")
        soup = BeautifulSoup(content, 'html.parser')
        print("++++++++++++++++++5+++++++++++++++++++++")
        # print("=============================soup================================",type(soup))
        # print(soup.text)
        # print(len(soup.text))
        if len(soup.text) == 0:
            # print("=============================soup================================",type(soup))
            # print("1")
            soup = BeautifulSoup(content,'html5lib')
            # print(len(soup.text))
        # print("=============================soup================================",type(soup))

        time =  url.split('/')[-2].replace('-','')
        # print("=============================time================================")
        # print(time)
        print(soup.find('title').text)
        title = soup.find('title').text.split(' ')[0]
        print("++++++++++++++++++6+++++++++++++++++++++")
        # print("=============================title================================")
        # print(title)
        div_lelvel_str = soup.find('div', id='artibody')
        p_level_list = div_lelvel_str.find_all('p')
        content_real = ''
        for item in p_level_list:
            content_real = content_real + item.text.strip()
        # print("=============================content==============================")
        print(content_real)
        print("++++++++++++++++++7+++++++++++++++++++++")
        news_tmp["_id"] = news_id.encode('utf8')
        news_tmp["title"] = title.encode('utf8')
        news_tmp["content"] = content_real.encode('utf8')
        news_tmp["time"] = time.encode('utf8')
        news_tmp["category"] = category.encode('utf8')

        # print(news_tmp)
        return news_tmp

def startmain(num):
    opt_opt = NewsJson('queue.json','visited.json')
    queue = opt_opt.get_queue()
    visited =opt_opt.get_visited()
    for i in range (0,num):
        begin_craw = Begin_crawler(str(i))
        begin_craw.start()




def get_url_test():

    # opt_opt = NewsJson('queue.json','visited.json')
    # queue = opt_opt.get_queue()
    # visited =opt_opt.get_visited()
    urltuple = ("test","http://ent.sina.com.cn/s/h/2016-12-06/doc-ifxyiayq2522965.shtml")
    content = requests.get(urltuple[1],timeout = 10).content
    soup = BeautifulSoup(content, 'html.parser')
    div_lelvel_str = soup.find('div', id='artibody')
    print(div_lelvel_str)
def readone():
    catch_tuple = ('娱乐','http://ent.sina.com.cn/tv/zy/2016-12-05/doc-ifxyiayr9116764.shtml')
    begin_craw = Begin_crawler("thread1")
    begin_craw.read_one_news(catch_tuple)
if __name__ == "__main__":
    CONDITION = threading.Condition()


    opt_opt = NewsJson('jsonfile/queue.json','jsonfile/visited.json')

    # queue = get_page_list(100,200)
    # opt_opt.save_queue(queue)

    threadnum = 1
    queue = opt_opt.get_queue()
    print(len(queue))
    visited =opt_opt.get_visited()
    print(len(visited))
    # for i in range (0,threadnum):
    #     begin_craw = Begin_crawler("thread: "+str(i))
    #     begin_craw.start()
