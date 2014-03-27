import dataset

def setup_db():
    queries = {
        "has_tables": 'SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=\'entries\') as exists;',
        "create_entries": """CREATE TABLE entries (
            id SERIAL NOT NULL, reddit_id TEXT, title TEXT, link TEXT, subreddit TEXT,
            downvotes INTEGER, mined_from TEXT, rank INTEGER,
            observed TIMESTAMP, upvotes INTEGER, article TEXT,
            PRIMARY KEY (id)
        );""",
        "create_index": """
        CREATE UNIQUE INDEX reddit_id_index ON entries(reddit_id);
        """
    }

    db = dataset.connect('postgresql://foobar:foobarbaz@testdb.cy2ub2trrp92.us-east-1.rds.amazonaws.com:5432/reddit')
    for item in db.query(queries['has_tables']):
        if not item['exists']:
            db.query(queries['create_entries'])
            db.query(queries['create_index'])
        break

    return db