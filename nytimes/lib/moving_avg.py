import sys
import json
import time
import redis

conn = redis.Redis()

while True:
    polarities = []
    subjectivities = []

    keys = conn.keys()
    for key in keys:
        try:
            print key
            polarity = conn.hget(key, 'polarity')
            subjectivity = conn.hget(key, 'subjectivity')
            polarities.append(float(polarity))
            subjectivities.append(float(subjectivity))
        except Exception as e:
            #there might not yet be a delta for this time
            #or the key might be the moving avg itself
            continue

    if len(polarities):
        avg_pol = sum(polarities)/float(len(polarities))
    else:
        avg_pol = 0

    if len(subjectivities):
        avg_subj = sum(subjectivities)/float(len(subjectivities))
    else:
        avg_subj = 0

    print avg_pol

    conn.set("movingAvgArticlePolarity", avg_pol)
    conn.set("movingAvgArticleSubjectivity", avg_subj)
    
    time.sleep(5)