# Getting Started 
## Getting the Dependencies
1. `export CFLAGS=-Qunused-arguments`
2. `export CPPFLAGS=-Qunused-arguments`
3. `pip install -r requirements.txt`

## Running the subreddit finder
`python subreddit_selector.py`

## Running the miner
1. Your IP needs to be added to the RDS security group, or you have to change `helpers/db.py` to point to your PostgreSQL db.
2. `python miner.py`
