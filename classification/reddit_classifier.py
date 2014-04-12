#!/usr/bin/env python

import sys
import psycopg2
import cPickle as pickle
import numpy as np
from scipy import sparse
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn import neighbors, naive_bayes
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

#Sources used: lab 5's prepare.py
#http://blog.mafr.de/2012/04/15/scikit-learn-feature-extractio/

REGEX = re.compile(r"\W+")
#TODO: use nltk tokenizer
def tokenize(text):
    return [tok.strip().lower() for tok in REGEX.split(text) if tok]

def get_data():
    subreddit = []
    upvotes = []
    downvotes = []
    data_train = []
    with open('TestFile.csv', 'r') as datafile:
        for line in datafile:
            row = line.strip().split(',')
            data_train.append(row[len(row)-1])
            subreddit.append(row[0])
            upvotes.append(row[1])
            downvotes.append(row[2])
                
    #data_train = np.recfromcsv('TestFile.csv', delimiter=',');
     
    #print data_train
    vec = CountVectorizer(tokenizer=tokenize)
    data = vec.fit_transform(data_train).toarray()
    data = np.array(np.column_stack([subreddit, upvotes, downvotes, data]))

    #print data
    X = data[:, 1:]
    y = data[:, 0]
    #print X
    #print y
    return (X, y)

def get_train_test():

    X, y = get_data()

    #TODO: Run cross validation
    X_train = X[:5, :]
    print X_train
    y_train = y[:5]
    print y_train
    X_test = X[[5], :]
    print X_test

    y_test = y[[5]]
    print y_test

    print '{} ({}%) training + {} ({}%) testing'.\
        format(len(y_train), 100.0*len(y_train)/len(y), \
                   len(y_test), 100.0*len(y_test)/len(y))
    return (X_train, y_train, X_test, y_test)

def eval(classifier):
    X_train, y_train, X_test, y_test = get_train_test()
    #print len(upvotes)
    #print upvotes
    classifier.fit(X_train, y_train)
    print classifier.predict(X_test)
    print 'train accuracy: {}'.format(classifier.score(X_train, y_train))
    print 'test accuracy: {}'.format(classifier.score(X_test, y_test))

#weight function for KNN -- not working.
def weight_upvotes(distances):
    #print "DISTANCES:"
    #print distances
    #for i in range(0, len(distances)):
    #    distances[i] /= int(upvotes[i])
    return distances


if __name__ == '__main__':
    #classifier = neighbors.KNeighborsClassifier(n_neighbors=1)#, weights=weight_upvotes)
    classifier = DecisionTreeClassifier(max_depth=5)
    eval(classifier)
