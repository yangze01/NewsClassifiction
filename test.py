#coding=utf-8
from bs4 import BeautifulSoup
import requests
import datetime
import html5lib
import time
import os
import re
import json
import sys
import re
import string
from newsOnMysql import *
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    # opt = NewsOnMysql()
    # a = opt.findall()[1][2]#.encode('utf8')
    # a="my name is john, i am a student in ncepu and bupt."
    # print(a)
    # b = a.translate(None, string.punctuation)
    # c=a.replace(string.punctuation,"")
    # d = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),)
    # print(b)
    # print(c)
    text = '一、二，三。四！五？'
    print(text)
    print(''.join(re.findall(u'[\u4e00-\u9fff]+', text)))
