import re
import os
import StringIO
import math

class MyTokenizer:
    def __init__(self, regexp):
        self.collection_size = 0
        self.reg = regexp
    def tokenize(self, text):
        from nltk.tokenize import RegexpTokenizer
        tokenizer = RegexpTokenizer(self.reg)
        tokens = tokenizer.tokenize(text)
        return tokens

    def store_words(self, dictionary, tokens):
        for token in tokens:
            if token in dictionary:
                dictionary[token] += 1
            else:
                dictionary[token] = 1
            self.collection_size += 1
    
    
def load_data():
    """
    Given a pathname of a directory, creates a list of strings out of the
    contents of the files in that directory.
    """
    data_strings=[]
    file_list=os.listdir(os.getcwd())
    for filename in file_list:
        pathname=os.path.join(os.getcwd(),filename)
        data_strings.append(open(pathname).read())
    return data_strings       

def run():
    re_all = '\d+\.?\d+|[\w]+|[^a-zA-Z0-9\s]'
    re_word_only = '[a-zA-Z]+'
    path = './'
    words = {}
    collection_size = 0
    sorted_list = []
    reviews = load_data()
    
    n = 1
    tokenizer = MyTokenizer(re_word_only)
    for review in reviews:
        tokens = tokenizer.tokenize(review)
        tokenizer.store_words(words, tokens)
        n += 1
        
    sorted_list = sorted(words.iteritems(), key = lambda item: item[1], reverse = True)
    dic_file = open('dict.txt', 'w')
    for i, item in enumerate(sorted_list):
        dic_file.write(str(i + 1) + ' ' + str(item) + '\n')
    dic_file.close()
    #print collection_size
    #print len(sorted_list)
    #print '\n'
    return tokenizer.collection_size, len(sorted_list)


n_tokens, n_terms = run()
print str(n_tokens) + ', ' + str(n_terms)

    
