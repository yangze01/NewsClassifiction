#-*- coding: UTF-8 -*-
import sys
reload(sys)
import json
sys.setdefaultencoding('utf8')
class WriteRead(object):
    def __init__(self,userdir):
        self.userdir = userdir
    def get_json_data(self):
        self.readf = open(self.userdir,'r')
        json_data = self.readf.read()
        self.readf.close()
        decode_json = json.loads(json_data)
        return decode_json
    def save2json(self,data2save):
        encode_json = json.dumps(data2save)
        self.writef = open(self.userdir,'w')
        self.writef.write(encode_json)
        self.writef.close()

if __name__ == "__main__":
    data1 = [1,2,3,4,5,6]
    opt_file = WriteRead('test.json')
    opt_file.save2json(data1)
    get_data = opt_file.get_json_data()
    print(type(get_data))
    for i in get_data:
        print(i)
