import json
import praw
# from collections import Counter
import time
import datetime
from datetime import timedelta
import datetime as dt
import os
from dotenv import load_dotenv
from cryptos import crypto_dict

from psaw import PushshiftAPI

load_dotenv()
final_dict = {}
words_collected = []
json_dump = []

def main():
    subName = "CryptoCurrency"

    today = dt.datetime.now()
    yesterday = int((today - timedelta(days=7)).timestamp())

    api = PushshiftAPI(setupReddit())
    gen = api.search_submissions(subreddit=subName, after=yesterday)
    results = list(gen)    

    print(len(results))

    for item in results:
        title = item.title.split(' ')
        for word in title:
            words_collected.append(word)

    fillFinalDict()
    # printFinalDict()
    writeDictToJSON()



def fillFinalDict():
    for word in words_collected:
        if word in crypto_dict.values():
            if word not in final_dict.keys():
                final_dict[word] = 1
            else:
                final_dict[word] += 1
    
    for item in final_dict:
        json_dump.append({"name": item, "count": final_dict[item]})
                

def printFinalDict():
    sorted_dict = dict(sorted(final_dict.items(), key=lambda x: x[1], reverse=True))
    for item in sorted_dict:
        print(f"{item}: {final_dict[item]}")

def writeDictToJSON():
    sorted_dict = sorted(json_dump, key=lambda x: x['count'], reverse=True)
    with open('./data/crypto_count.json', 'w') as f:
        json.dump(sorted_dict, f)

def setupReddit():
    reddit_client_id = os.getenv('reddit_client_id')
    reddit_client_secret = os.getenv('reddit_secret')
    reddit_username = os.getenv('reddit_username')
    reddit_password = os.getenv('reddit_password')

    reddit = praw.Reddit(client_id=reddit_client_id,
                        client_secret=reddit_client_secret,
                        username=reddit_username,
                        password=reddit_password,
                        user_agent='Nillocs_Scraper')

    return reddit


if __name__ == '__main__':
    main()