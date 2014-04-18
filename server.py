import json

from flask import Flask, send_from_directory, request
from helpers.EntryParser import EntryParser

app = Flask(__name__)
entry_parser = EntryParser()

url_map = {}
fake_answer = {
	'books': 0.63,
	'music': 0.24,
	'news': 0.17,
	'politics': 0.13,
	'science': 0.33,
	'technology': 0.97,
	'todayilearned': 0.23,
	'worldnews': 0.19
}

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

			# TODO: get actual numbers from data instead of using the fake answer

			url_map[url] = json.dumps({
				'title': title,
				'data': { key: value for key, value in fake_answer.iteritems() }
			})
			return url_map[url]
	except Exception, e:
		return json.dumps({ 'error': 'could not parse link and/or content'}), 400

if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)