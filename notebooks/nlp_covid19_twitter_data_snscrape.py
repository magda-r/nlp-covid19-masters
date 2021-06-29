
#%%
import os
import pandas as pd
import snscrape.modules.twitter as sntwitter
from datetime import datetime
from datetime import timedelta 

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
# Scraping tweets from a text search query - day after day
# Creating list to append tweet data to
tweets_daily_df = pd.DataFrame()

max_per_day = 10
date_since = datetime(2020,3,1)
date_until = datetime(2021,4,30)

# Using TwitterSearchScraper to scrape data and append tweets to list
while(date_since <= date_until):
    tweets_per_day = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('covid OR coronavirus OR  \
        corona OR virus OR pandemic OR vaccine OR vaccinated OR lockdown OR quarantine \
        filter:retweets filter:replies since:'+ date_since.strftime("%Y-%m-%d") + ' until:' \
        + (date_since + timedelta(days=1)).strftime("%Y-%m-%d") + ' lang:en').get_items()):

            if i > max_per_day:
                break
            tweets_per_day.append([tweet.id, 
                                tweet.content, 
                                tweet.date, 
                                tweet.replyCount,
                                tweet.retweetCount,
                                tweet.likeCount,
                                tweet.user.displayname, 
                                tweet.user.location, 
                                tweet.user.followersCount])
    
    # Creating a dataframe from the tweets list above
    tweets_per_day_df = pd.DataFrame(tweets_per_day, columns=['id', 
                                                            'text', 
                                                            'date',
                                                            'no_replies',
                                                            'no_retweets',
                                                            'no_likes',
                                                            'user',
                                                            'location', 
                                                            'no_followers'])
    tweets_daily_df = pd.concat([tweets_daily_df, tweets_per_day_df])
    tweets_daily_df = tweets_daily_df.reset_index(drop=True)

    date_since = date_since + timedelta(days=1)

# %%
# Scraping tweets from a text search query - hour after hour
# Creating list to append tweet data to
# tweets_hourly_df = pd.DataFrame()

# max_per_hour = 15
# date_since = datetime(2020,3,1,0,0,0)
# date_until = datetime(2020,3,1,23,59,59)

# # Using TwitterSearchScraper to scrape data and append tweets to list
# while(date_since <= date_until):
#     tweets_per_hour = []

#     for i, tweet in enumerate(sntwitter.TwitterSearchScraper('covid OR coronavirus OR  \
#         corona OR virus OR pandemic OR vaccine OR vaccinated OR lockdown OR quarantine \
#         -filter:retweets -filter:replies since:'+ date_since.strftime("%Y-%m-%d %H:%M:%S") + ' until:' \
#         + (date_since + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S") + ' lang:en').get_items()):

#             if i > max_per_hour:
#                 break
#             tweets_per_hour.append([tweet.id, 
#                                 tweet.content, 
#                                 tweet.date, 
#                                 tweet.replyCount,
#                                 tweet.retweetCount,
#                                 tweet.likeCount,
#                                 tweet.user.displayname, 
#                                 tweet.user.location, 
#                                 tweet.user.followersCount])
#     # print(date_since.strftime("%Y-%m-%d %H:%M:%S"))
#     # print((date_since + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))

#     # Creating a dataframe from the tweets list above
#     tweets_per_hour_df = pd.DataFrame(tweets_per_hour, columns=['id', 
#                                                             'text', 
#                                                             'datetime',
#                                                             'no_replies',
#                                                             'no_retweets',
#                                                             'no_likes',
#                                                             'user',
#                                                             'location', 
#                                                             'no_followers'])
#     # print(tweets_per_hour_df)                                                        
#     tweets_hourly_df = pd.concat([tweets_hourly_df, tweets_per_hour_df])

#     date_since = date_since + timedelta(hours=1)

# %%
tweets_daily_df['date'] = pd.to_datetime(tweets_daily_df['date'], format="%Y-%m-%d")
tweets_daily_df
# %%
tweets_daily_df.to_csv("../data/covid19_tweets_snscrape_daily_rt.csv", index=False)

# %%
