import requests
from bs4 import BeautifulSoup
import json
import nltk

class EntryParser(object):
    URL_PREFIX = "https://readability.com/api/content/v1/parser"
    API_TOKEN = "f4d14c4595eb09d217e729334340e615970c2ba7"

    def _get_data(self,link):
        response = requests.get(EntryParser.URL_PREFIX, params={
            'url': link,
            'token': EntryParser.API_TOKEN 
        }, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
        }, timeout=2)

        if response.content is None:
            raise requests.exceptions.RequestException()

        return response.json()

    def get_content(self, link):
        data = self._get_data(link)
        return nltk.clean_html(data['content'])

    def get_title_and_content(self, link):
        data = self._get_data(link)
        return data['title'], nltk.clean_html(data['content'])