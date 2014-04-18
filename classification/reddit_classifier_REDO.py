#!/usr/bin/env python

import sys
import nltk
import cPickle as pickle
import numpy as np
from scipy import sparse
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn import metrics
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
import tldextract
from sklearn.feature_selection.univariate_selection import chi2
from sklearn.feature_selection import SelectKBest
from scipy.stats import sem
from sklearn.pipeline import Pipeline
from nltk.corpus import wordnet
import string
import csv
csv.field_size_limit(sys.maxsize)
#Sources used: lab 5's prepare.py
#http://blog.mafr.de/2012/04/15/scikit-learn-feature-extractio/
#http://stackoverflow.com/questions/22077046/how-to-normalize-ranked-data-in-scikit-learn

classifiers = [ LinearSVC(),  OneVsRestClassifier(LinearSVC(random_state=0)), MultinomialNB(),
KNeighborsClassifier(n_neighbors=5)]

redditStopWords = [line.strip() for line in open("RedditStopWords.txt")]
#[MultinomialNB(alpha=0.5), OneVsRestClassifier(LinearSVC(random_state=0)),
#RandomForestClassifier(n_estimators = 100)]
#one vs rest class linear svc 0.5
	
   #[KNeighborsClassifier(1)] ]
  #  [BernoulliNB(), MultinomialNB(), OneVsRestClassifier(LinearSVC(random_state=0)),
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

#def tokenize(text):
#   return [stemmer.stem(token) for token in nltk.word_tokenize(text)]
    
def get_data():
    subreddits = []
    upvotes = []
    downvotes = []
    url_domains = []
    url_suffixes = []
    data = []

#TestFile.csv
    with open('NewRedditSampleAll.csv', 'r') as datafile:
	reader = csv.reader(datafile)
        for row in reader:
	    if row[0] in ['todayilearned','news']: continue
	    #if tldextract.extract(row[3]).domain == 'twitter': continue
	    #if len(tokenize(row[len(row)-1]))<100: continue
            data.append(row[len(row)-1])
	    
            subreddits.append(row[0]) 
            upvotes.append(row[1])
            downvotes.append(row[2])
            #url_domains.append(tldextract.extract(row[3]).domain)
	    #url_suffixes.append(tldextract.extract(row[3]).suffix)
                
    #split data into training and test sets
    test_fraction = 0.2
    x_train, x_test, y_train, y_test = train_test_split(data, subreddits, test_size=test_fraction, random_state=2)
    tfv = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    #CountVectorizer(tokenizer=tokenize, stop_words='english')
    
    classifier = LinearSVC()

    clf = Pipeline([ ('vect', tfv), ('clf',classifier) ])
    evaluate_cross_validation(clf, x_train, y_train, 5)
        
    print
    print
    
    #train the clf classifier and asses its accuracy
    clf.fit(x_train, y_train)
    print 'accuracy on training set = ', clf.score(x_train, y_train)
    print 'accuracy on testing  set = ', clf.score(x_test, y_test)
    y_pred = clf.predict(x_test)
    print metrics.classification_report(y_test, y_pred)
    print 'confusion matrix'
    print metrics.confusion_matrix(y_test, y_pred)
    print
    
    print_top10(tfv, classifier, sorted(list(set(subreddits))))
    
def print_top10(vectorizer, clf, class_labels):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    for i, class_label in enumerate(class_labels):
        top10 = np.argsort(clf.coef_[i])[-10:]
        print("%s: %s" % (class_label,
              " ".join(feature_names[j] for j in top10)))

   #div = DictVectorizer()
   # X = []
    
#set up the classifier
def evaluate_cross_validation(clf, x, y, K):
    cv = cross_validation.KFold(len(y), K, shuffle=True, random_state=0)
    scores = cross_validation.cross_val_score(clf, x, y, cv=cv)
    print scores
    print ("mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))



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

    
    #clf = Pipeline([('chi2', SelectKBest(chi2, k=1000)),
    #            ('classifier', classifier)])
    #multi_clf = OneVsRestClassifier(clf)
    get_data()
#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#
#    classifier.fit(X_train, y_train)
#    print "Accuracy: %0.2f " % classifier.score(X_test, y_test)
#   
#    scores = cross_validation.cross_val_score(classifier, X, y, cv=3)
#    print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)    
    #scores = cross_validation.cross_val_score(multi_clf, X, y, cv=3)
    #print scores
    #print("accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

   # print 'train accuracy: {}'.format(classifier.score(X_train, y_train))
   # print 'test accuracy: {}'.format(classifier.score(X_test, y_test))

#weight function for KNN -- not working. predict function???
def weight_upvotes(distances):
    #print "DISTANCES:"
    #print distances
    #for i in range(0, len(distances)):
    #    distances[i] /= int(upvotes[i])
    return distances

if __name__ == '__main__':
    #classifier = neighbors.KNeighborsClassifier(n_neighbors=1)#, weights=weight_upvotes)
    #classifier = DecisionTreeClassifier(max_depth=5)
       # X, y = get_data()
#	for classifier in classifiers:
 #   		eval(classifier, X, y)
    get_data()
