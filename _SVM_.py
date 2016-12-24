# coding=utf-8
import sys
import os
# sys.path.append('C:\Users\john\Desktop\spider\NewsClassifiction\libsvm-3.21\python');
# os.chdir('C:\Users\john\Desktop\spider\NewsClassifiction\libsvm-3.21\python')
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

    train_file = 'C:\Users\john\Desktop\spider\NewsClassifiction\\train.txt'
    test_file = 'C:\Users\john\Desktop\spider\NewsClassifiction\\test.txt'
    model_file = 'C:\Users\john\Desktop\spider\NewsClassifiction\\svm_model'
    # y_train,x_train = svm_read_problem(train_file)
    y_test,x_test = svm_read_problem(test_file)

    # svm_model = svm_train(y_train,x_train,'-t 3 -c 5')
    # svm_save_model(model_file,svm_model)
    print(y_test)
    mymodel = svm_load_model(model_file)
    p_label, p_acc, p_val = svm_predict(y_test, x_test, mymodel)
    print(p_label,p_acc,p_val)
