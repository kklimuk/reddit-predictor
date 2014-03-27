import requests

from bs4 import BeautifulSoup

class EntryParser(object):
    INVISIBLE_ELEMENTS = set(['style', 'script', '[document]', 'head', 'title'])

    def is_visible(self, element):
        if element.parent.name in EntryParser.INVISIBLE_ELEMENTS:
            return False
        return True

    def get_content(self, link):
        visible = filter(self.is_visible, BeautifulSoup(requests.get(link).text).findAll(text=True))
        return ' '.join(' '.join(visible).split())