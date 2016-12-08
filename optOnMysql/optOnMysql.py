#coding=utf-8
import pymysql
import sys
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

if __name__ == "__main__":

    opt_connect = OptOnMysql()
    test = opt_connect.exeQuery("select * from news")
    for i in test:
        print(i[1])
