import json
import praw
# from collections import Counter
from datetime import timedelta
import datetime as dt
import os
from dotenv import load_dotenv
from psaw import PushshiftAPI

load_dotenv()

def customTracker(subName, wordList, days):
    final_dict = {}
    words_collected = []
    json_dump = []

    print(subName, wordList, days)

    wordList = [word.lower() for word in wordList]

    today = dt.datetime.now()
    lastweek = int((today - timedelta(days=days)).timestamp())

    api = PushshiftAPI(setupReddit())
    gen = api.search_submissions(subreddit=subName, after=lastweek)
    results = list(gen)    

    for item in results:
        title = item.title.split(' ')
        for word in title:
            words_collected.append(word.lower())

    fillFinalDict(wordList, words_collected, final_dict, json_dump)

    return sorted(json_dump, key=lambda x: x['count'], reverse=True)


def fillFinalDict(wordList, words_collected, final_dict, json_dump):
    for word in words_collected:
        if word in wordList:
            if word not in final_dict.keys():
                final_dict[word] = 1
            else:
                final_dict[word] += 1
    
    for item in final_dict:
        json_dump.append({"name": item, "count": final_dict[item]})
                

def printFinalDict(final_dict):
    sorted_dict = dict(sorted(final_dict.items(), key=lambda x: x[1], reverse=True))
    for item in sorted_dict:
        print(f"{item}: {final_dict[item]}")

def writeDictToJSON(json_dump):
    sorted_dict = sorted(json_dump, key=lambda x: x['count'], reverse=True)
    with open('./data/custom_count.json', 'w') as f:
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

