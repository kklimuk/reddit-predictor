#Description of files
-miner.py was our first attempt to mine posted articles in subreddits  
-scraper.js is our second attempt to scrape the article links and metadata. It's used in conjunction with Reddit Enhancement Suite and injected into the browser. The collected data is in the json folder.  
-jsonparser.js takes those jsons of article urls, scraped those urls using Readability API and populated our DB  
-classification folder includes the final classifier testing script (as well as an earlier V1 script) that ran  classifier cross validations.  
-classification folder also includes NewRedditSampleAll.csv that is our complete and final scraped data of 9 subreddits.  
-prediction folder includes the pickled best classifier and vectorizer, as well as prediction code is now integrated into server.py  
-server.py runs our web application (URL is localhost:5000) 

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
