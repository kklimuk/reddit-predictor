import requests

from urlparse import urlparse
from bs4 import BeautifulSoup

class SubredditParser(object):
    PROHIBITED_DOMAINS = ['imgur','instagram', 'flickr', 'photobucket', 'memebase', '9gag', 'failblog', 'quickmeme', 'youtube', 'vimeo']
    PROHIBITED_FORMATS = ['gif', 'jpeg', 'jpg', 'png']

    def __init__(self, reddit):
        self.reddit = reddit
        self.url = 'http://www.reddit.com' + ('/r/%s/top' % self.reddit if self.reddit is not None else '')


    def parse_entries(self, limit=100, after=''):
        unfiltered = self.get_dataset(self.get_document(after, limit))
        return filter(self.filter, unfiltered)


    def get_document(self, after, limit):
        return BeautifulSoup(requests.get(self.url, params={
            "limit": limit,
            "after": after,
            "sort": "top",
            "t": "all"
        }).text)

    def get_dataset(self, document):
        return filter(
            lambda entry: entry and entry['rank'],
            map(self.get_entry, document.find_all(class_='thing'))
        )

    def get_entry(self, html_entry):
        title = html_entry.find('a', 'title')
        if title is None:
            return False

        comments = html_entry.find(class_='comments').string.split(' ')[0]
        subreddit = html_entry.find(class_='subreddit')
        rank = html_entry.find(class_='rank').string

        return {
            "reddit_id": filter(lambda x: 'id-' in x, html_entry['class'])[0][3:],
            "title": title.string,
            "link": title['href'],
            "subreddit": subreddit.string if subreddit else '',
            "upvotes": int(html_entry['data-ups']),
            "downvotes": int(html_entry['data-downs']),
            "mined_from": self.reddit,
            "rank": int(rank) if rank else 0
        }

    def filter(self, entry):
        parsed_url = urlparse(entry['link'])
        if not parsed_url.netloc:
            return False

        for prohibited in SubredditParser.PROHIBITED_FORMATS:
            if prohibited in parsed_url.path:
                return False

        for prohibited in SubredditParser.PROHIBITED_DOMAINS:
            if prohibited in parsed_url.netloc:
                return False
        return True