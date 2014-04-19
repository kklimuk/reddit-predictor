#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import nltk
import cPickle as pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from nltk.stem.porter import PorterStemmer
import tldextract
import string


ALPHABET = '^[a-zA-Z]+$'
redditStopWords = [line.strip() for line in open("RedditStopWords.txt")]
subreddits = ['books','music','politics','science','technology','television','worldnews']
    
def clean(text):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text).strip()

def tokenize(text):
    tokens = []
    for token in nltk.wordpunct_tokenize(text):
        token = clean(token)
        if len(token)>2 and re.match(ALPHABET,token) and token not in redditStopWords:
        	tokens.append(token)
    return tokens

def predict_subreddits(data):
    #convert all chars to unicode
    if isinstance(data, str):
        data = unicode(data, errors='ignore')
    
    prediction_map = {}
    classifier, vect = load_best()    
    #transform using loaded vectorizer
    X_test = vect.transform([data])

    print classifier.predict(X_test)

    predictions = classifier.decision_function(X_test)
    
    for i, subreddit in enumerate(subreddits):
        prediction_map[subreddit] = predictions[0][i]
    
    return prediction_map

def load_best():
	f = open('84linearsvcClassify.pickle')
	classifier = pickle.load(f)
	f.close()
	
        f = open('84linearsvcVect.pickle')
	vect = pickle.load(f)
	f.close()
	
	return classifier,vect


if __name__ == '__main__':
    sample = \
'''

Apps
enterprise apps
Why Your Favorite App Isn’t Business-Related And How It Can Be
Posted 3 hours ago by Todd McKinnon (@toddmckinnon)

    More

Next Story

Editor’s note: Todd McKinnon is CEO of identity management firm Okta.

Think about your favorite app. Let me guess. It’s a consumer app — something like Uber, Instagram or Pinterest. So what do we do to get business apps into that list of favorites?

It’s rare to hear end users rave about an enterprise app that’s useful, simple, engaging and (dare I say) emotional – particularly all at the same time. We have some work to do if we want to perfect the enterprise user experience, which is why we should learn from beloved consumer products. If we put the user experience first and incorporate utility, simplicity, engagement and emotion into our products, we can make work just as easy and delightful as posting a photo.
Utility: What would you do without it?

The most important aspect of the user experience is utility. The design, simplicity and engagement of an app don’t matter if the app isn’t useful. As Brian Hansen, our UX architect at Okta, says, the key to creating a product people love is to create something they didn’t even know they needed and now can’t live without.

Take the various (and now abundant) transportation-related apps like Uber, Lyft and Waze, for example. A few years ago, if you were using your phone to get a ride to the office or the airport, you were probably calling a cab company. Now a ride just about anywhere is only a few clicks away, and if your driver doesn’t know the best way, or wants to check the traffic, that only takes a few seconds on your phone, too. Users love Uber, Lyft and Waze because they’re useful – they enhance your travel and driving experiences so much so that I’d venture to guess you haven’t dialed Yellow Cab in months, maybe years.

How can cloud providers learn from their success? We should strive to create an experience so useful that users can’t imagine working without it. Asana is already doing that with project management – with some users abandoning email entirely, saying, “Asana or bust” after getting up and running with their workflow solution. dotloop is another that has revolutionized how people work in real estate, encouraging almost 1 million agents and brokers to trade in FAX machines and scanners for cloud software – and creating the opportunity to get deals done on their mobile devices.
'''
    print predict_subreddits(sample)
