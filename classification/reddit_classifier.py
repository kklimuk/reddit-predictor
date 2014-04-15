#!/usr/bin/env python

import sys
import nltk
import psycopg2
import cPickle as pickle
import numpy as np
from scipy import sparse
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.neighbors import KNeighborsClassifier
from sklearn import naive_bayes
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import BernoulliNB 
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsOneClassifier

#Sources used: lab 5's prepare.py
#http://blog.mafr.de/2012/04/15/scikit-learn-feature-extractio/

classifiers = [OneVsRestClassifier(LinearSVC(random_state=0)), BernoulliNB(), MultinomialNB(),
KNeighborsClassifier(), RandomForestClassifier(n_estimators = 100)]
#[MultinomialNB(alpha=0.5), OneVsRestClassifier(LinearSVC(random_state=0)),
#RandomForestClassifier(n_estimators = 100)]
#one vs rest class linear svc 0.5
	
   #[KNeighborsClassifier(1)] ]
  #  [BernoulliNB(), MultinomialNB(), OneVsRestClassifier(LinearSVC(random_state=0)),
#OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=0),
#OneVsOneClassifier(LinearSVC(random_state=0))],
   # [SVC(kernel='linear')], [RandomForestClassifier(n_estimators = 100)]]
stemmer = PorterStemmer()
def tokenize(text):
    return [stemmer.stem(token) for token in nltk.word_tokenize(text)]

def get_data():
    subreddit = []
    upvotes = []
    downvotes = []
    data= []
#TestFile.csv
    with open('UpdatedRedditSm.csv', 'r') as datafile:
        for line in datafile:
            row = line.strip().split(',')
            data.append(row[len(row)-1])
            subreddit.append(row[0])
            #upvotes.append(row[1])
            #downvotes.append(row[2])
	     #uncomment above and change column stack params
                
    #data= np.recfromcsv('UpdatedReddit.csv', delimiter=',');
     
    #print data
    #vec = CountVectorizer(tokenizer=tokenize, stop_words='english')
    vec = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    X = vec.fit_transform(data).toarray()
    y = np.array(subreddit)

    #X = data[:, 1:]
    #y = data[:, 0]
    print X
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

def save_best_classifier(classifier):
	f = open('my_classifier.pickle', 'wb')
	pickle.dump(classifier, f)
	f.close()

def load_best_classifier():
	f = open('my_classifier.pickle')
	classifier = pickle.load(f)
	f.close()
	return classifier

def eval(classifier, X, y):
    #X_train, y_train, X_test, y_test = get_train_test()
    #print len(upvotes)
    #print upvotes
    #classifier.fit(X_train, y_train)
    #print classifier.predict(X_test)

    scores = cross_validation.cross_val_score(classifier, X, y, cv=5)
    print scores
    print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

   # print 'train accuracy: {}'.format(classifier.score(X_train, y_train))
   # print 'test accuracy: {}'.format(classifier.score(X_test, y_test))

#weight function for KNN -- not working.
def weight_upvotes(distances):
    #print "DISTANCES:"
    #print distances
    #for i in range(0, len(distances)):
    #    distances[i] /= int(upvotes[i])
    return distances

if __name__ == '__main__':
    #classifier = neighbors.KNeighborsClassifier(n_neighbors=1)#, weights=weight_upvotes)
    #classifier = DecisionTreeClassifier(max_depth=5)
        X, y = get_data()
	for classifier in classifiers:
    		eval(classifier, X, y)
