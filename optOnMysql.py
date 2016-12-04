import pymysql
class OptOnMysql(object):

    def __init__(self):
        self.db_host = ''
        self.db_user = ''
        self.db_passowrd = ''
        self.db_name = ''
        # self.conn = ''
        # self.cur = '' 
        # self.db_opt_blog_unit = ''
        #-----------------********************-----------------#
    def connect2Mysql(self, db_host, db_user, db_passowrd, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_passowrd = db_passowrd
        self.db_name = db_name
        try:
            self.conn = pymysql.connect(host=self.db_host,user=self.db_user,passwd=self.db_passowrd,db=self.db_name)
            self.cur = self.conn.cursor()
            print("connect %s %s success!!"%(self.conn,self.cur))
            # print(conn,cur)
            return 1
        except :
            print("connect failure!!"%(self.conn,self.cur))
            return 0

    def test_find(self,time):
        alllist =  self.cur.execute("select * from news where time = %s"%time)
        return alllist
if __name__ == "__main__":
    db_host = "localhost"
    db_user = "root"
    db_passowrd = "1234"
    db_name = "sina_news"
    opt_connect = OptOnMysql()
    test = opt_connect.test_find("20161202")
    print(test)
