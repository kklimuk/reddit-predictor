import requests
from bs4 import BeautifulSoup
import json
#import html2text
import nltk

URL_PREFIX = "https://readability.com/api/content/v1/parser?url="
API_TOKEN = "&token=26e64a97b42cb7576765eab70f7a64d6e10b524d"

class EntryParser(object):
    #INVISIBLE_ELEMENTS = set(['style', 'script', '[document]', 'head', 'title'])


    #def is_visible(self, element):
    #    if element.parent.name in EntryParser.INVISIBLE_ELEMENTS:
    #        return False
    #    return True

    def get_content(self, link):
        #visible = filter(self.is_visible, BeautifulSoup(requests.get(link).text).findAll(text=True))
	#return ' '.join(' '.join(visible).split())
	response = requests.get(URL_PREFIX + link + API_TOKEN)
	return nltk.clean_html(response.json()['content'])
