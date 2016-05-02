# moving_avg.py
#
# This script is used for keeping a moving average of the sentiment
# values for today's articles, polarity and subjectivity.
# This is done by getting all of the values stored in the redis DB
# and then calculating averages and storing them as new keywords in redis.

# Import required libraries
import sys
import json
import time
import redis

# create redis connection
conn = redis.Redis()

while True:
    polarities = []
    subjectivities = []

    # Run through all of the sentiment values for today's articles
    # appending their values to an array
    keys = conn.keys()
    for key in keys:
        try:
            print key
            polarity = conn.hget(key, 'polarity')
            subjectivity = conn.hget(key, 'subjectivity')
            polarities.append(float(polarity))
            subjectivities.append(float(subjectivity))
        except Exception as e:
            # ignore invalid keys
            continue

    # Calculate today's polarity and subjectivity averages using the array
    if len(polarities):
        avg_pol = sum(polarities)/float(len(polarities))
    else:
        avg_pol = 0

    if len(subjectivities):
        avg_subj = sum(subjectivities)/float(len(subjectivities))
    else:
        avg_subj = 0

    print avg_pol

    # Enter current averages into redis
    conn.set("movingAvgArticlePolarity", avg_pol)
    conn.set("movingAvgArticleSubjectivity", avg_subj)
    
    # sleep for a minute
    time.sleep(60)
