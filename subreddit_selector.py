import requests
import json
import logging

from bs4 import BeautifulSoup
from time import sleep
from random import randint
from helpers.SubredditParser import SubredditParser

THRESHOLD = 5

def html_mapper(row):
    cells = row.select('td')
    if len(cells) > 0:
        return cells[1].text.lower()
    return None

def parse_subreddits(document):
    return filter(lambda entry: entry, map(html_mapper, document.select('#yw2 tr')))

def main(total):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='subreddits.log',level=logging.DEBUG)

    page = 1
    accepted = 0
    with open('subreddits.txt', 'w') as f:
        while accepted < total:
            document = BeautifulSoup(requests.get('http://www.redditlist.com/page-%d' % page).text)

            parsed = parse_subreddits(document)
            for subreddit in parsed:
                entries = SubredditParser(subreddit).parse_entries(100)
                if len(entries) > THRESHOLD:
                    accepted += 1
                    f.write(subreddit + '\n')
                    f.flush()
                    logging.info("Added: Subreddit %s, article count %d" % (subreddit, len(entries)))
                else:
                    logging.info("Rejected: Subreddit %s, article count %d" % (subreddit, len(entries)))

                if accepted >= total:
                    break

                sleep(randint(1, 3))

            page += 1

if __name__ == "__main__":
    main(250)