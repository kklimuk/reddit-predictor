#!/usr/bin/env python

import string
import sys
import nltk
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
from sklearn.feature_extraction import DictVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import BernoulliNB 
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.preprocessing import normalize
import csv
csv.field_size_limit(sys.maxsize)
import tldextract

#Sources used: lab 5's prepare.py
#http://blog.mafr.de/2012/04/15/scikit-learn-feature-extractio/

redditStopWords = [line.strip() for line in open("RedditStopWords.txt")]
#[MultinomialNB(alpha=0.5), OneVsRestClassifier(LinearSVC(random_state=0)),
#RandomForestClassifier(n_estimators = 100)]
#one vs rest class linear svc 0.5

   #[KNeighborsClassifier(1)] ]
  # [BernoulliNB(), MultinomialNB(), OneVsRestClassifier(LinearSVC(random_state=0)),
#OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=0),
#OneVsOneClassifier(LinearSVC(random_state=0))],
   # [SVC(kernel='linear')], [RandomForestClassifier(n_estimators = 100)]
REGEX = '^[a-zA-Z]+$'
stemmer = PorterStemmer()
def clean(text):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text).strip()

def tokenize(text):
    #print [token for token in nltk.wordpunct_tokenize(text)]
    tokens = []
    for token in nltk.wordpunct_tokenize(text):
        token = clean(token)
        if len(token)>2 and re.match(REGEX,token) and token not in redditStopWords:
         tokens.append(token)
    #print tokens
    #print len(tokens)
    return tokens
def get_data():
    upvotes = []
    downvotes = []
    data = []
    url_domains = []
    subreddits = [] 
    featureDict = {}
#TestFile.csv
    with open('NewRedditSampleAll.csv', 'r') as datafile:
        reader = csv.reader(datafile)
        for row in reader:
	    if len(tokenize(row[len(row)-1]))<100: continue
	    if row[0] in ['todayilearned','news']: continue
            data.append(row[len(row)-1])
            subreddits.append(row[0]) 
            upvotes.append(row[1])
            downvotes.append(row[2])
            url_domains.append(tldextract.extract(row[3]).domain)
                
    tfv = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    div = DictVectorizer()
    
    X = []
    
    # fit/transform the TfidfVectorizer on the training data
    vect = tfv.fit_transform(data)
    
    for i in range(len(upvotes)):
        feature_dict = {'upvotes': upvotes[i], 'downvotes':downvotes[i],
                        'url_domain':url_domains[i]}
        # get ith row of the tfidf matrix (corresponding to sample)
        row = vect.getrow(i)    
    
        # filter the feature names corresponding to the sample
        all_words = tfv.get_feature_names()
        words = [all_words[ind] for ind in row.indices] 
    
        # associate each word (feature) with its corresponding score
        word_score = dict(zip(words, row.data)) 
    
        # concatenate the word feature/score with the datamining feature/value
        X.append(dict(word_score.items() + feature_dict.items()))
    #normalized = normalize(div.fit_transform(X), norm='l1', axis=1)
    return (div.fit_transform(X).toarray(), np.array(subreddits))  # training data based on tfidf features and metadata

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
    X, y = get_data()
    eval(LinearSVC(), X, y)

