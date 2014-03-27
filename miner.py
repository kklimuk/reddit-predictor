import logging

from datetime import datetime
from threading import Thread
from time import sleep

from helpers.EntryParser import EntryParser
from helpers.SubredditParser import SubredditParser
from helpers.db import setup_db


def mine(db, mined_from=None, entry_count=200, sleep_total=600):
    subreddit_parser = SubredditParser(mined_from)
    entry_parser = EntryParser()
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='miner.log',level=logging.DEBUG)

    last_id = ""
    step_size = entry_count / 10
    for count in xrange(0, entry_count, step_size):
        skipped = False

        entries = subreddit_parser.parse_entries(step_size, last_id)
        for i, entry in enumerate(entries):
            if i == len(entries) - 1:
                last_id = entry['reddit_id']

            saved_entry = db['entries'].find_one(reddit_id=entry['reddit_id'])

            if saved_entry is None:
                try:
                    entry['article'] = entry_parser.get_content(entry['link'])
                except Exception, e:
                    logging.error(e)
                    continue

                db['entries'].insert(entry)
            else:
                skipped = True
                logging.info('Skipped entries %d-%d in %s' % (count, count + (entry_count / 10) - 1, mined_from))
                break

            sleep(0.1)

        if not skipped:
            logging.info('Finished mining entries %d-%d in %s' % (count, count + (entry_count / 10) - 1, mined_from))


def main():
    threads = []
    db = setup_db()

    with open('subreddits.txt') as f:
        SUBREDDITS = f.read.split('\n')

    for index in xrange(0, len(SUBREDDITS), 4):
        for x in xrange(index, index + 4):
            if x >= len(SUBREDDITS):
                break
            thread = Thread(target=mine, args=(db,), kwargs={ "mined_from": SUBREDDITS[x] })
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        threads = []


if __name__ == "__main__":
    main()

