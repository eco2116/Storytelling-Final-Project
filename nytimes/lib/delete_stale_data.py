# delete_stale_data.py
#
# This script deletes articles in the redis DB that are older than a day.
# This is helpful for performing today's sentiment analysis on articles.

# import necessary libaries
import sys
import redis
import time

# Set time to live to 1 day for the articles
TTL = 86400 

# Create redis connection
conn = redis.Redis()

while True:
	# Get all keys (times of articles)
	keys = conn.keys()
	current_time = time.time()
	for key in keys:
		try:
			# Remove article record if it was from over a day ago
			# This ensures sentiment analysis and most postivie/negative
			# articles only come from this day
			if(current_time - float(key)  > TTL):
				conn.delete(key)
		except ValueError as e:
			# If you come across an invalid key, ignore it
			continue;

	# Sleep for a minute
	time.sleep(60)
