# coding=utf-8
import sys
import itertools
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import gensim
from collections import Counter
import cPickle
import os
import json
import numpy as np
import sys
BasePath = sys.path[0]
reload(sys)
sys.setdefaultencoding('utf8')

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
    cate_dict = {'股市':0,'财经':1,'国际':2,'科技':3,'军事':4,'社会':5,'体育':6,'国内':7,'美股':8,'娱乐':9,'娱乐':10,'其他':11}

    x_text = get_json_data(BasePath + "/jsonfile/courpus.json")[0:2000]
    y_text = get_json_data(BasePath + "/jsonfile/cate_list.json")[0:2000]

    y = [cate_dict[tmp.encode("utf8")] for tmp in y_text]
    # TODO y convert to int
    print("_________________________________________________")
    print(type(x_text),type(np.array(y)))
    print("-------------------------------------------------")

    return [x_text,np.array(y)]

def load_vocab(sen_word):
    vocab = []
    for word_list in sen_word:
        # print(word_list)
        vocab.extend(word_list)
    vocab = set(vocab)
    return vocab

def load_bin_vec(fname, vocab):
    """
        加载300*1 word2vec from my model
        个人感觉原函数有点奇怪，之后可以修改
    """
    word_vecs = {}
    with open(fname,"rb") as f:
        header = f.readline()
        vocab_size,layer1_size =map(int,header.split())#???map是什么意思
        print(vocab_size,layer1_size)
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in xrange(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch !='\n':
                    word.append(ch)
            if word in vocab:
                word_vecs[word] = np.fromstring(f.read(f.read(binary_len),dtype = 'float32'))
            else:
                f.read(binary_len)
    return word_vecs

def get_W(word_vecs, k = 300):
    """
        Get word matrix. W[i] is the vector for word indexed by i
        把单词建成索引进行查找，问：它和直接查找词区别在哪？
    """
    vocab_size = len(word_vecs)
    word_idx_map = dict()
    W = np.zeros(shape = (vocab_size + 1,k),dtype = 'float32')
    W[0] = np.zeros(k,dtype = 'float32')
    i = 1
    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
    return W,word_idx_map

def add_unknown_words(word_vecs,vocab,k=300):
    """
        设置未知词的词向量
    """
    for word in vocab:
        if word not in word_vecs:
            word_vecs[word] = np.random(-0.25,0.25,k)
    return word_vecs

def batch_iter(data,batch_size, num_epochs, shuffle = True):
    """
        Generates a batch iterator for a dataset
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
            # shuffled_data=np.random.permutation(data)
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index] # yield

def load_train_dev_data():
    print("Loading data...")
    x_text,y = load_data_and_labels()
    #Randomly shuffle data
    np.random.seed(10)
    shuffle_indices = np.random.permutation(np.arange(len(y)))
    x_text = np.array(x_text)
    print(type(x_text[0]))
    x_text = x_text[shuffle_indices]
    y_shuffled = y[shuffle_indices]
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(type(x_text[0]))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    max_sentence_length = max([len(x) for x in x_text])
    # Load set word
    word_set = load_vocab(x_text)
    # Load word2vec
    if os.path.exists(BasePath + "/jsonfile/Word2Vec"):
        # wor2vec_model = cPickle.load(open(BasePath + "/jsonfile/Word2Vec","rb"))
        fname = BasePath + "/jsonfile/Word2Vec"
        wor2vec_model = gensim.models.Word2Vec.load(fname)

    else:
        wor2vec_model = load_bin_vec(BasePath + "GoogleNews-vectors-negative300.bin", word_set)
        wor2vec_model = add_unknown_words(wor2vec_model, word_set, 300)
        cPickle.dump(wor2vec_model, open(BasePath + "/jsonfile/Word2Vec", "wb"))
    x = []
    print("~+~+~+~+~+~+~++~+~++~+~+~+~+~+~+~+~+~+")
    print(len(wor2vec_model["股市".decode("utf8")]))
    print("~+~+~+~+~+~+~++~+~++~+~+~+~+~+~+~+~+~+")
    for words in x_text:
        # words = ste.split()
        # print(words)
        # words = words[0:2]
        # print(words)
        l = len(words)

        sentence = []
        for i, word in enumerate(words):
            # print(word)
            sentence.append(wor2vec_model[word])

        zeros_list = [0] * 300

        for j in range(max_sentence_length - i - 1):
            sentence.append(zeros_list)
        x.append(sentence)
    print(len(sentence[0]))
    print("typetypetypetypetypetypetypetypetypetypetypetypetypetypetypetypetypetype")
    print(type(x))
    x = np.array(x)

    # Split train/test set
    # TODO: This is very crude, should use cross-validation

    x_train, x_dev = x[:-1000], x[-1000:]
    # print(x_train)
    y_train, y_dev = y_shuffled[:-1000], y_shuffled[-1000:]
    print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))
    print(type(x_train),type(y_train))
    return x_train,y_train,x_dev,y_dev







if __name__ == "__main__":
    # positive_examples = list(open(BasePath + "/jsonfile/courpus.json", "r").readlines())

    # x_text = get_json_data(BasePath + "/jsonfile/courpus.json")[0]
    # y = get_json_data(BasePath + "/jsonfile/cate_list.json")[0]
    # print(x_text)
    # print(cate_dict[y.encode('utf8')])

    x_train,y_train,x_dev,y_dev = load_train_dev_data()
    # print(type(x_train[0][1]))
