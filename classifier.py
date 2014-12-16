from __future__ import division
from math import log
import os
import re
import pick


re_all = '\d+\.?\d+|[\w]+|[^a-zA-Z0-9\s]'
re_word = '[\w]+|!'
keywords = pick.run()

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

class Naive_Bayes(object):
    def __init__(self, data, feature_function):
        """
        Takes a dictionary mapping labels to lists of strings with that label, and a function which
        produces a list of feature values from a string.
        """
        self.function = feature_function
        # key: class; value: number of samples belonging to this class
        self.labels = {}
        # dicts: every dictionary corresponds to a class
        # in every dictionary, key is a word, value is the number of samples in which this word appears
        self.dicts = {}
        self.word_space = {}
        # every key is a class
        for key in data:
            self.labels[key] = 0
            dictionary = {}
            word_number = 0
            for string in data[key]:
                self.labels[key] += 1
                words = feature_function(string)
                for word in words:
                    if word in dictionary:
                        freq = dictionary[word]
                        dictionary[word] = freq + 1
                    else:
                        word_number += 1
                        dictionary[word] = 1
            self.word_space[key] = word_number
            #print "word_space[%s]: %d" %(key, word_number)
            self.dicts[key] = dictionary
        # key: class; value: P(class)
        self.prior_label = {}
        # total number of samples in all classes
        total_samples = 0
        for label in self.labels:
            total_samples += self.labels[label]
        for label in self.labels:
            self.prior_label[label] = self.labels[label] / total_samples
            #print "%s, %d" %(label, self.labels[label])
            #print "prior prob[%s]: %f" %(label, self.prior_label[label])
    
    

    def classify(self, string):
        """
        Classifies a string according to the feature function and training data
        provided at initialization.
        """
        words = self.function(string)
        # key: class; value: P(class | string)
        result = {}
        for label in self.labels:
            space = self.labels[label]
            prob = 0
            for word in words:
                if word in self.dicts[label]:
                    prob += log(self.dicts[label][word] / space)
                else:
                    prob += log(0.2 / space)
            for feature in self.dicts[label]:
                if feature not in words:
                    if self.dicts[label][feature] == space:
                        prob += log(0.2 / space)
                    else:
                        prob += log(1 - self.dicts[label][feature] / space)
            result[label] = prob + log(self.prior_label[label])
            #print "result[%s] = %e" %(label, result[label])
 
        for label in result:
            max_prob = result[label]
            max_class = label
            break
        for label in result:
            if result[label] > max_prob:
                max_prob = result[label]
                max_class = label
        assert max_prob < 0
        #print "max_class: ", max_class
        return max_class
        

def pick_words(string):
    global keywords
    words = []
    tokenizer = MyTokenizer(re_word)
    for word in tokenizer.tokenize(string):
        if word in keywords:
            if word not in words:
                words.append(word)
    return words

def bag_of_words(string):
    
    tokenizer = MyTokenizer(re_word)
    words = tokenizer.tokenize(string)
    return list(set(words))
    
def load_data(directory):
    """
    Given a pathname of a directory, creates a list of strings out of the
    contents of the files in that directory.
    """
    data_strings=[]
    file_list=os.listdir(directory)
    for filename in file_list:
        pathname=os.path.join(directory,filename)
        data_strings.append(open(pathname).read())
    return data_strings

def print_evaluation(classifier, test_data):
    """
    Takes a classifier and a dictionary mapping labels to lists of test strings.
    Prints accuracy, precision, and recall scores for the classifier.
    """
    wrong = open('wrong.txt', 'w')
    scores={}
    correct=0
    total=0
    labels=test_data.keys()
    for label in labels:
        scores[label]={"true_pos":0,"true_neg":0,"false_pos":0,"false_neg":0}
    for label in test_data:
        # print "label: ", label
        for string in test_data[label]:
            classification=classifier.classify(string)
            total+=1
            #print label, classification
            if classification == label:
                # print "classification correct"
                correct+=1
                scores[label]["true_pos"]+=1
                # print "true_pos: ",scores[label]["true_pos"] 
                for other_label in labels:
                    if other_label != label:
                        scores[other_label]["true_neg"]+=1
            else:
                info = 'should be:' + label + '\n' + string + '\n'
                wrong.write(info)
                scores[label]["false_neg"]+=1
                scores[classification]["false_pos"]+=1
                for other_label in labels:
                    if other_label != label and other_label != classification:
                        scores[other_label]["true_neg"]+=1

        
    print "Accuracy: " + str(correct/total)
    for label in labels:
        true_pos=scores[label]["true_pos"]
        # print "true_pos: ", scores[label]["true_pos"]
        false_pos=scores[label]["false_pos"]
        true_neg=scores[label]["true_neg"]
        false_neg=scores[label]["false_neg"]
        print str(label)
        precision=true_pos/(true_pos+false_pos)
        recall=true_pos/(true_pos+false_neg)
        print "\tPrecision: " + str(precision)
        print "\tRecall: " + str(recall)
        print "\tF-Measure: " + str(2*precision*recall/(precision+recall))
    wrong.close()
        
                

def run():
    trainset = {'pos': load_data('movie_train/pos'), 'neg': load_data('movie_train/neg')}
    testset= {'pos': load_data('movie_test/pos'), 'neg': load_data('movie_test/neg')}
    classifier = Naive_Bayes(trainset, pick_words)
    print_evaluation(classifier, testset)

run()
