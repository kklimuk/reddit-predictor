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
redditStopWords = [line.strip() for line in open("./classification/RedditStopWords.txt")]
subreddits = ['books','music','politics','science','technology','television','worldnews']
	
def clean(text):
	return re.sub('[%s]' % re.escape(string.punctuation), '', text).strip()

def tokenize(text):
	tokens = []
	for token in nltk.wordpunct_tokenize(text):
		token = clean(token)
		if len(token) >2 and re.match(ALPHABET,token) and token not in redditStopWords:
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

	predictions = classifier.decision_function(X_test)
	
	for i, subreddit in enumerate(subreddits):
		prediction_map[subreddit] = predictions[0][i]
	
	return prediction_map

def load_best():
	f = open('./prediction/84linearsvcClassify.pickle')
	classifier = pickle.load(f)
	f.close()
	
	f = open('./prediction/84linearsvcVect.pickle')
	vect = pickle.load(f)
	f.close()
	
	return classifier, vect

import json

from flask import Flask, send_from_directory, request
from helpers.EntryParser import EntryParser
app = Flask(__name__)
entry_parser = EntryParser()

url_map = {}

@app.route('/')
def index():
	return send_from_directory('./', 'index.html')

@app.route('/classify', methods=['POST'])
def classifier():
	try:
		url = request.get_json()['url']
		if url in url_map:
			return url_map[url]
		else:
			title, data = entry_parser.get_title_and_content(url)
			answer = predict_subreddits(data)

			url_map[url] = json.dumps({
				'title': title,
				'data': { key: value for key, value in answer.iteritems() }
			})
			return url_map[url]
	except Exception, e:
		return json.dumps({ 'error': 'could not parse link and/or content'}), 400

if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)