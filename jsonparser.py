import json
import logging

from time import sleep
from random import shuffle

from helpers.db import setup_db
from helpers.EntryParser import EntryParser
from os import listdir


parsed = []
for f in listdir('./json'):
    with open('./json/%s' % f) as data:
        parsed.extend(json.loads(data.read()))
shuffle(parsed)


db = setup_db()
entry_parser = EntryParser()


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='miner.log',level=logging.DEBUG)
for entry in parsed:
    saved_entry = db['entries'].find_one(reddit_id=entry['reddit_id'])
    
    if saved_entry is None:
        entry['article'] = None
        try:
            entry['article'] = entry_parser.get_content(entry['link'])
            db['entries'].insert(entry)
        except Exception, error:
            logging.error('Error: %s %s %s' % (entry['mined_from'], entry['link'], error))
            continue

    sleep(0.5)
