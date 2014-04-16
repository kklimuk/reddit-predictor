import requests
from bs4 import BeautifulSoup
import json
import nltk

class EntryParser(object):
    URL_PREFIX = "https://readability.com/api/content/v1/parser"
    API_TOKEN = "26e64a97b42cb7576765eab70f7a64d6e10b524d"

    def get_content(self, link):
        response = requests.get(EntryParser.URL_PREFIX, params={
            'url': link,
            'token': EntryParser.API_TOKEN 
        }, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
        }, timeout=0.5)

        if response.content is None:
            raise requests.exceptions.RequestException()

        return nltk.clean_html(response.json()['content'])
