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
from sklearn.svm import LinearSVC
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

#This class does the actual cross-validation testing of classifiers.
#author: Austin

#Sources used:
#lab 5's prepare.py
#http://blog.mafr.de/2012/04/15/scikit-learn-feature-extractio/
#http://gemelli.spacescience.org/~hahnjm/data_science/abstracts/abstracts.py
#http://stackoverflow.com/questions/19466868/how-do-i-do-classification-using-tfidfvectorizer-plus-metadata-in-practice
#http://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers

classifiers = [
	#BernoulliNB(),
	#BernoulliNB(alpha=0.5),
	#MultinomialNB(),
	#MultinomialNB(alpha=0.5),
	#KNeighborsClassifier(n_neighbors=3),
	#LinearSVC(C=2),
	#LinearSVC(C=10),
	#LinearSVC(C=100),
	#KNeighborsClassifier(n_neighbors=5)
	LinearSVC()
 ]

redditStopWords = [line.strip() for line in open("RedditStopWords.txt")]
REGEX = '^[a-zA-Z]+$'
#stemmer = PorterStemmer()

def clean(text):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text).strip()

def tokenize(text):
    #return [token for token in nltk.wordpunct_tokenize(text)]
    tokens = []
    for token in nltk.wordpunct_tokenize(text):
        token = clean(token)
        if len(token)>2 and re.match(REGEX,token) and token not in redditStopWords:
            tokens.append(token)
    #print tokens
    #print len(tokens)
    return tokens

def run_tests():
    subreddits = []
    upvotes = []
    downvotes = []
    url_domains = []
    url_suffixes = []
    data = []

    with open('NewRedditSampleAll.csv', 'r') as datafile:
	reader = csv.reader(datafile)
        for row in reader:
            #include only 7 subreddits, so exclude the following 2.
	    if row[0] in ['todayilearned','news']: continue
            if tldextract.extract(row[3]).domain == 'twitter': continue
            #exclude articles under 100 tokens
      	    if len(tokenize(row[len(row)-1]))<100: continue
	    data.append(row[len(row)-1])
	    subreddits.append(row[0])
	    #upvotes.append(row[1])
	    #downvotes.append(row[2])
	    #url_domains.append(tldextract.extract(row[3]).domain)	
	    #url_suffixes.append(tldextract.extract(row[3]).suffix)
	#X = np.hstack([upvotes,downvotes,data])

	for classifier in classifiers:
	    crossvalidate(classifier, data, subreddits)
	
def crossvalidate(classifier, data, subreddits):
    print classifier	
	
    #split data into training and test sets
    test_fraction = 0.2
    x_train, x_test, y_train, y_test = train_test_split(data, subreddits, test_size=test_fraction, random_state=2)

    tfv = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    # CountVectorizer(tokenizer=tokenize, stop_words='english')

    clf = Pipeline([ ('vect', tfv), ('clf',classifier) ])
    evaluate_cross_validation(clf, x_train, y_train, 5)
        
    print
    print
    
    #train the clf classifier and asses its accuracy
    clf.fit(x_train, y_train)
    print 'accuracy on training set = ', clf.score(x_train, y_train)
    print 'accuracy on testing set = ', clf.score(x_test, y_test)
    y_pred = clf.predict(x_test)
    print metrics.classification_report(y_test, y_pred)
    print 'confusion matrix'
    print metrics.confusion_matrix(y_test, y_pred)
    print
    
    print_top10(tfv, classifier, sorted(list(set(subreddits))))

 #http://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers   
def print_top10(vectorizer, clf, class_labels):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    for i, class_label in enumerate(class_labels):
        top10 = np.argsort(clf.coef_[i])[-10:]
        print("%s: %s" % (class_label,
              " ".join(feature_names[j] for j in top10)))
    
def evaluate_cross_validation(clf, x, y, K):
    cv = cross_validation.KFold(len(y), K, shuffle=True, random_state=0)
    scores = cross_validation.cross_val_score(clf, x, y, cv=cv)
    print str(K) + "-fold cross validation:"
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

if __name__ == '__main__':
    run_tests()
