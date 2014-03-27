import requests
import json
from bs4 import BeautifulSoup

def html_mapper(row):
    cells = row.select('td')
    if len(cells) > 0:
        return cells[1].text.lower()
    return None

def parse_subreddits(document):
    return filter(lambda entry: entry, map(html_mapper, document.select('#yw2 tr')))

def main(total):
    subreddits = []

    page = 1
    while len(subreddits) < total:
        document = BeautifulSoup(requests.get('http://www.redditlist.com/page-%d' % page).text)
        subreddits.extend(parse_subreddits(document))
        page += 1

    print json.dumps(subreddits, indent=2)

if __name__ == "__main__":
    main(250)