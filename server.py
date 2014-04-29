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
redditStopWords = [ line.strip() for line in open("./classification/RedditStopWords.txt") ]
subreddits = ['books','music','politics','science','technology','television','worldnews']
	
def clean(text):
	return re.sub('[%s]' % re.escape(string.punctuation), '', text).strip()

def tokenize(text):
	tokens = []
	for token in nltk.wordpunct_tokenize(text):
		token = clean(token)
		if len(token) > 2 and re.match(ALPHABET,token) and token not in redditStopWords:
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
	
	feature_names = vect.get_feature_names()
	features = sorted({ 
		feature_names[feature_index]: X_test.data[index] \
		for index, feature_index in enumerate(X_test.indices) 
	}.items(), key=lambda entry: entry[1], reverse=True)

	return prediction_map, features[:20]


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
		if url not in url_map:
			title, data = entry_parser.get_title_and_content(url)
			prediction, salient_words = predict_subreddits(data)

			url_map[url] = json.dumps({
				'title': title,
				'data': {
					'prediction': { key: value for key, value in prediction.iteritems() },
					'salient_words': salient_words
				}
			})

		return url_map[url], 200, {
			'Content-Type': 'application/json'
		}
	except Exception, e:
		return json.dumps({ 'error': 'could not parse link and/or content'}), 400, {
			'Content-Type': 'application/json'
		}

if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)