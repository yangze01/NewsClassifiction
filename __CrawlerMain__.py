#coding=utf-8
from bs4 import BeautifulSoup
from optOnMysql.NewsOnMysql import *
from optOnMysql.NewsUnit import *
from writeRead.WriteRead import *
from writeRead.NewsJson import *
from Crawler.Begin_Crawler import *
from Crawler.page_list import *
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
    queue_filename = 'C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\queue.json'
    visited_filename = 'C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\visited.json'
    opt_opt = NewsJson(queue_filename,visited_filename)

    threadnum = 1
    queue = opt_opt.get_queue()
    print(len(queue))
    visited =opt_opt.get_visited()
    print(len(visited))
