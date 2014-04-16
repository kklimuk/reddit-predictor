import logging
from requests.exceptions import Timeout

from datetime import datetime
from threading import Thread
from time import sleep
from random import randint

from helpers.EntryParser import EntryParser
from helpers.SubredditParser import SubredditParser
from helpers.db import setup_db

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='miner.log',level=logging.DEBUG)

def mine(db, mined_from=None, entry_count=200):
    subreddit_parser = SubredditParser(mined_from)
    entry_parser = EntryParser()

    ids = set([])
    last_id = ""

    step_size = entry_count / 10
    count = 0
    accepted = 0

    while accepted < entry_count:
        entries = None
        while entries is None:
            try:
                entries = subreddit_parser.parse_entries(step_size, last_id)
            except Timeout, error:
                logging.error('Timeout: %s %s %s' % (mined_from, count, error))
                sleep(randint(10, 20))
            except Exception, error:
                logging.error("Error: %s %s" % (mined_from, error))
                sleep(randint(10, 20))

        unchanged = False
        skipped = False
        for i, entry in enumerate(entries):
            if entry['reddit_id'] in ids:
                unchanged = True
                logging.info('Unchanged: entries %d-%d in %s' % (i, count + len(entries) - 1, mined_from))
                break

            last_id = entry['reddit_id']
            ids.add(last_id)

            saved_entry = db['entries'].find_one(reddit_id=entry['reddit_id'])
            
            if saved_entry is None:
                entry['article'] = None
                while entry['article'] is None:
                    try:
                        entry['article'] = entry_parser.get_content(entry['link'])
                        db['entries'].insert(entry)
                        accepted += 1
                    except Exception, error:
                        logging.error("Error: %s %s" % (mined_from, error))
                        sleep(randint(2, 4))
            else:
                skipped = True
                logging.info('Skipped: %d-%d in %s' % (i, count + len(entries) - 1, mined_from))
                break

            sleep(0.65)

        if unchanged:
            break
        elif not skipped:
            logging.info('Finished: entries %d-%d in %s' % (count, count + len(entries) - 1, mined_from))

        count += len(entries)


def main():
    threads = []
    db = setup_db()

    with open('subreddits.txt') as f:
        SUBREDDITS = f.read().split('\n')

    for index in xrange(0, len(SUBREDDITS), 4):
        for x in xrange(index, index + 4):
            if x >= len(SUBREDDITS):
                break
            thread = Thread(target=mine, args=(db,), kwargs={ "mined_from": SUBREDDITS[x] })
            thread.start()
            threads.append(thread)
            sleep(1)

        for i, thread in enumerate(threads):
            logging.info('Finished thread: %s' % SUBREDDITS[index + i])
            thread.join()

        threads = []


if __name__ == "__main__":
    main()

