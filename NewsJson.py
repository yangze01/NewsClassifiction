#-*- coding: UTF-8 -*-
import sys
reload(sys)
import json
from WriteRead import *
sys.setdefaultencoding('utf8')
class NewsJson(object):
    def __init__(self,queuedir,visiteddir):
        self.opt_queue = WriteRead(queuedir)
        self.opt_visited = WriteRead(visiteddir)
    def get_queue(self):
        queue = self.opt_queue.get_json_data()
        print("the queue length is:"+str(len(queue)))
        return queue
    def get_visited(self):
        visited = self.opt_visited.get_json_data()
        print("the visited length is:"+str(len(visited)))
        return set(visited)
    def save_queue(self,data2save):
        self.opt_queue.save2json(data2save)
    def save_visited(self,data2save):
        self.opt_visited.save2json(data2save)
