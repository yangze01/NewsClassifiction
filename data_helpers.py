# coding=utf-8
import os
import sys
reload(sys)
import json
import gensim
import cPickle
import logging
import itertools
import numpy as np
BasePath = sys.path[0]
sys.setdefaultencoding('utf8')
from collections import Counter
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def load_data_and_labels():
    """
        加载数据和标签
    """
    cate_dict = {'股市':0,'财经':1,'国际':2,'科技':3,'军事':4,'社会':5,'体育':6,'国内':7,'美股':8,'娱乐':9,'其他':10}

    x_text = get_json_data(BasePath + "/jsonfile/title_courpus.json")[0:]
    y_text = get_json_data(BasePath + "/jsonfile/cate_list.json")[0:]
    y = list()
    tmp_y = [cate_dict[tmp.encode("utf8")] for tmp in y_text]
    for tmp_num in tmp_y:
        tmp = np.zeros(12)
        tmp[tmp_num] = 1
        # print(tmp)
        y.append(tmp)
    x_ret = [' '.join(cut_sen) for cut_sen in x_text]
    print("!~!~!~!~!~!~!~!~!~!~!~!~!~!~!")
    print(x_ret[0])
    return [x_ret,np.array(y)]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
def load_vocab(sentences):
    vocab=[]
    for sentence in sentences:
        vocab.extend(sentence.split())
    vocab=set(vocab)
    return vocab

def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    with open(fname, "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        print(vocab_size,layer1_size)
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in xrange(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)
            if word in vocab:
                word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
            else:
                f.read(binary_len)
    return word_vecs



def get_W(word_vecs, k=300):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """

    vocab_size = len(word_vecs)
    word_idx_map = dict()
    W = np.zeros(shape=(vocab_size + 1, k), dtype='float32')
    W[0] = np.zeros(k, dtype='float32')
    i = 1

    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
        i += 1
    return W, word_idx_map

def add_unknown_words(word_vecs, vocab, k=300):
    """
    For words that occur in at least min_df documents, create a separate word vector.
    0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
    """
    for word in vocab:
        if word not in word_vecs:
            word_vecs[word] = np.random.uniform(-0.25, 0.25, k)
    return word_vecs

if __name__ == "__main__":
    x,y = load_data_and_labels()
    # print(x[0])

    # positive_examples = list(open(BasePath + "/jsonfile/courpus.json", "r").readlines())
    #
    # x_text = get_json_data(BasePath + "/jsonfile/courpus.json")[0:2]
    # y = get_json_data(BasePath + "/jsonfile/cate_list.json")[0:2]
    # # print(type(x_text))
    # # print(type(y))
    # # print(cate_dict[y.encode('utf8')])
    #
    # get_predict_data(x_text,y)
    # # x_train,y_train,x_dev,y_dev = load_train_dev_data()
    # # print(x_train[0])
    # # print(y_train[0])
    # # print(type(x_train[0][1]))
