# coding=utf-8
import sys
import os
BasePath = sys.path[0]
sys.path.append(BasePath + '/libsvm-3.22/python');
os.chdir(BasePath + '/libsvm-3.22/python')
from svmutil import *
reload(sys)
sys.setdefaultencoding('utf8')
import json
def get_json_data(userdir):
    readf = open(userdir,'r')
    json_data = readf.read()
    readf.close()
    decode_json = json.loads(json_data)
    return decode_json

def save2json(userdir,data2save):
    encode_json = json.dumps(data2save)
    writef = open(userdir,'w')
    writef.write(encode_json)
    writef.close()

if __name__ == "__main__":

    train_file = BasePath + '/train.txt'
    test_file = BasePath + '/test.txt'
    model_file = BasePath + '/svm_model'
    y_train,x_train = svm_read_problem(train_file)
    print(x_train[0])
    y_test,x_test = svm_read_problem(test_file)
    print("load data finished")
    svm_model = svm_train(y_train,x_train,'-t 3 -c 5 -h 0')
    svm_save_model(model_file,svm_model)
    print(y_test)
    mymodel = svm_load_model(model_file)
    p_label, p_acc, p_val = svm_predict(y_test, x_test, mymodel)
    print(p_label,p_acc,p_val)
