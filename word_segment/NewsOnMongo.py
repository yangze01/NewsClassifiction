# coding=utf-8
import sys
import re
import pymongo
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')

class NewsOnMongo():
    def __init__(self):
        self.db_uri= ''
        self.db_name= ''
        self.xlient = ''
        self.db = ''
        self.db_opt_segs_unit = ''
    def connect2Mongo(self,db_url,db_name):
        '''
            description:
                connect to the mongodb in python by db's uri
            input:
                db_name: name of mongodb to be connected
                db_uri: the uri of specified mongodb,
                        like "mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]"
            output:
                return statue number: 0:fail; 1:success
        '''
        self.db_uri = db_uri
        self.db_name = db_name
        #try connect to the specified mongodb
        try:
            self.xlient = MongoClient(self.db_uri)
            self.db = self.xlient[self.db_name]
            self.testResult = self.db.test123.find()
            for self.doc in self.testResult:
                print self.doc

            #self.address = self.xlient.client.address
            print "connect %s success!!" % self.db_name
            return 1
        except :
            print "connect %s failure!!" % self.db_name
            return 0

    def insert_segs2mongo(self,dbInstance,segs_unit):
        '''
            description:
                insert a segs to mongodb
            input:
                dbInstance: instance of mongodb to insert
                user_unit: user unit to be inserted

            output:
                return statue number: 0:fail; 1:success
        '''
        self.db = dbInstance
        self.db_opt_segs_unit = segs_unit
        self.db_opt_old_segs_unit = self.db.seg.find_one({"_id":self.db_opt_segs_unit["_id"]})
        if self.db_opt_segs_unit:
            print("user is exist!!")
        else:
            try:
                self.result = self.db.seg.insert_one(self.db_opt_segs_unit)
                print(self.result.inserted_id)
                # self.user.find(self.db_opt_segs_unit)
                print("insert success!")
                return 1
            except:
                print("insert failure!")
                return 0

if __name__ == "__main__":
    
