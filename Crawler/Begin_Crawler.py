#coding=utf-8
from bs4 import BeautifulSoup
from optOnMysql.NewsOnMysql import *
from optOnMysql.NewsUnit import *
from writeRead.WriteRead import *
from writeRead.NewsJson import *
import requests
import html5lib
import os
import re
import sys
import threading
import os
reload(sys)
sys.setdefaultencoding('utf8')

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
