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

if __name__ == "__main__":
    a = ['1','2','3','4','5']
    b = ['a','b','c','d','e']

    # c = [i + j for i,j in zip(a,b)]

    c = zip(a,b)
    d = ('1','a')
    for i in c:
        print i
