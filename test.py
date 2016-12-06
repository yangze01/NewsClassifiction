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
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    # a = ['1','2','3','4','5']
    # b = ['a','b','c','d','e']
    # c = {1,2,3,4}
    # print(a.pop())
    # a.append("123")
    # print(a)
    TIMESTAMP = time.strftime('%Y%m%d')
    

    # print(type(c))
    # # c = [i + j for i,j in zip(a,b)]
    # json_data = json.dumps(list(c))
    # print(type(json_data))
    # decode = json.loads(json_data)
    # print(type(set(decode)))
    #
    # while a:
    #     a.pop()
    #     print a
