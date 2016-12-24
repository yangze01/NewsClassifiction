#!/usr/bin/python
#-*- coding: UTF-8 -*-
import pymongo
from pymongo import MongoClient
import time
# from paper_Unit import *
import pdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class PaperOnMongo(object):
    '''
        operations on mongodb in python,
        like connect, insert, find, updata, delete
    '''
    def __init__(self):
        self.db_uri= ''
        self.db_name= ''
        self.xlient = ''
        self.db = ''
        self.db_opt_paper_unit = ''

    def connect2Mongo(self, db_uri, db_name):
        '''
            description:
                connect to the mongodb in python by db's uri
            input:
                db_name: name of mongodb to be connected
                db_uri: the uri of specified mongodb,
                        like "mongodb://[papername:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]"
            output:
                return statue number: 0:fail; 1:success
        '''
        self.db_uri = db_uri
        self.db_name = db_name
        #try connect to the specified mongodb
        try:
            self.xlient = MongoClient(self.db_uri)
            self.db = self.xlient[self.db_name]
            # self.testResult = self.db.paper.find()
            # for self.doc in self.testResult:
            #     print self.doc

            #self.address = self.xlient.client.address
            print "connect %s success!!" % self.db_name
            return 1
        except :
            print "connect %s failure!!" % self.db_name
            return 0
    def insertPaper2Mongo(self,dbInstance,paper_unit):
        self.db = dbInstance
        self.db_opt_paper_unit = paper_unit
        self.db_opt_old_paper_unit = self.db.paper.find_one({"_id":self.db_opt_paper_unit['_id']})
        if self.db_opt_old_paper_unit:
            print 'paper is exist!! update now!!'
            self.updataPaper2Mongo(self.db, self.db_opt_old_paper_unit, self.db_opt_paper_unit)
        else:

            try:
                #del self.db_opt_paper_unit['_id']
                self.result = self.db.paper.insert_one(self.db_opt_paper_unit)
                print self.result.inserted_id
                self.db.paper.find(self.db_opt_paper_unit)
                print "insert success!!"
                return 1
            except :
                print "insert failure!!"
                return 0
    def updataPaper2Mongo(self, dbInstance, old_paper_unit, new_paper_unit):
        '''
            description:
                updata the old_paper_unit to new_paper_unit on mongodb

            input:
                dbInstance: instance of mongodb to updata
                old_paper_unit: old paper unit content
                new_paper_unit: new paper unit content to updata into mongodb

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance

        self.old_paper_unit = old_paper_unit
        self.new_paper_unit = new_paper_unit

        try:

            self.result = self.db.paper.replace_one(
                self.old_paper_unit,
                self.new_paper_unit
            )
            #self.db.paper.find(self.new_paper_unit)
            print "updata success!!"
            print "matched count: %d" % self.result.matched_count
            print "modified count: %d" % self.result.modified_count
            return 1
        except :
            print "update failure!!"
            return 0


    #-----------------********************-----------------#
    def deletePaper2Mongo(self, dbInstance, delete_paper_condition):
        '''
            description:
                delete papers specified delete_paper_condition in dbInstance

            input:
                dbInstance: db instance of mongodb to delete
                delete_paper_condition: the matched paper

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.delete_paper_condition = delete_paper_condition

        try:
            self.result = self.db.paper.delete_one(self.delete_paper_condition)
            #print "delete matced count: %" % self.result.matched_count
            print "delete count: %d" % self.result.deleted_count
            print "delete success!!"
            return 1
        except :
            print "delete failure!!"
            return 0

    #-----------------********************-----------------#
    def getPaper2Mongo(self, dbInstance, get_paper_condition, get_paper_unit):
        '''
            description:
                get papers specified get_paper_condition in dbInstance

            input:
                dbInstance: db instance of mongodb to get
                get_paper_condition: the matched paper condition
                get_paper_unit: storage the papers matched condition

            output:
                return statue number: 0:fail; 1:success
        '''
        self.db = dbInstance
        self.get_paper_condition = get_paper_condition
        self.get_paper_unit = []
        self.paper_number = 0
        try:
            self.result = self.db.paper.find(self.get_paper_condition)
            for self.db_opt_paper_unit in self.result :
                self.paper_number += 1
                self.get_paper_unit.append(self.db_opt_paper_unit)

            ##get_paper_unit = self.get_paper_unit
            print "get paper count: %d" % self.paper_number
            ##print self.get_paper_unit
            print "get paper success!!"
            return self.get_paper_unit
        except :
            print "get paper failure!!"
            return 0
