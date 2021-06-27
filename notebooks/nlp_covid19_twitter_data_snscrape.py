
#%%
import os
import pandas as pd
import snscrape.modules.twitter as sntwitter

# %%
# Using OS library to call CLI commands in Python
os.system("snscrape --jsonl --max-results 500 --since 2020-03-01 twitter-search\
     \"covid until:2021-04-30\" > ../data/text-query-tweets.json")

# Reads the json generated from the CLI commands above and creates a pandas dataframe
tweets_df = pd.read_json('../data/text-query-tweets.json', lines=True)

# %%
# Scraping a specific twitter user’s tweets
# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:jack').get_items()):
    if i>100:
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    
# Creating a dataframe from the tweets list above 
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# %%
# Scraping tweets from a text search query
# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper('covid OR coronavirus OR  \
    corona OR virus OR pandemic OR vaccine OR vaccinated OR lockdown OR quarantine \
    -filter:retweets -filter:replies since:2020-03-01 until:2021-04-30 lang:en').get_items()):

    if i>5000:
        break
    tweets_list2.append([tweet.id, 
                        tweet.content, 
                        tweet.date, 
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.likeCount,
                        tweet.user.displayname, 
                        tweet.user.location, 
                        tweet.user.followersCount])
    
# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['id', 
                                                'text', 
                                                'datetime',
                                                'no_replies',
                                                'no_retweets',
                                                'no_likes',
                                                'user',
                                                'location', 
                                                'no_followers'])

# %%
tweets_df2

# %%
tweets_df2.to_csv("../data/covid19_tweets_snscrape.csv", index=False)

# %%
