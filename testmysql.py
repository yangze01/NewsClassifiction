#coding=utf-8
import pymysql
import sys
from NewsUnit import *
reload(sys)
sys.setdefaultencoding('utf8')
class OptOnMysql(object):

    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_passowrd = "1234"
        self.db_name = "sina_news"
        try:
            self.conn = pymysql.connect(host=self.db_host,user=self.db_user,passwd=self.db_passowrd,db=self.db_name,charset='utf8')
            self.cur = self.conn.cursor()
            print("connect %s %s success"%(self.conn,self.cur))
        except:
            print("connect %s %s fail"%(self.conn,self.cur))
        #-----------------********************-----------------#
    def exeUpdate(self,sql):
        sta = self.cur.execute(sql)
        self.conn.commit()
        return (sta)

    def exeDeleteById(self,sql,ID):
        sta = 0
        sta = self.cur.execute(sql%(int(ID)))
        return(sta)

    def exeQuery(self,sql):
        self.cur.execute(sql)
        return(self.cur)

    def connClose(self):
        self.cur.close()
        self.conn.close()


class NewsOnMysql(object):
    def __init__(self):
        self.db.user_unit = ""
        self.opt_OnMySql = OptOnMysql()
    def deleteById(self,id):
        sta = self.opt_OnMySql.exeDeleteById("delete from news where id=%d",id)
        return sta
    def deleteByIds(self,ids):
        sta = 0
        for eachID in ids:
            sta += self.deleteById(eachID)
        return sta
    def insertNews(self,news_unit):



    def findById(self,id):
        cur = self.opt_OnMySql.exeQuery("select * from news where id=%d"%int(id))
        it = cur.fetchall()
        len_it = len(it)
        if len_it == 0:
            print("there is nothing found.")
            return 0
        else:
            print(it)
            return 1


if __name__ == "__main__":
    id = '2'
    title = "今日说法"
    content = "我的名字叫张三，今年10岁了"
    opt = OptOnMysql()
    cur = opt.findById(id)
    opt.connClose()
