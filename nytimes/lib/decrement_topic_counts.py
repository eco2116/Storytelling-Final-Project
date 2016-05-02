# decrement_topic_counts.py
#
# This script is used for decrementing the keywords by 1 count
# each day so that more popular keywords of the day will remain
# in the redis DB for a longer duration.

# Import necessary dependencies
import redis # for decrementing from database
import time # for sleeping

# Setup redis connection
conn = redis.Redis()

# This decrementation will happen once a day
TTL = 86400 

while 1:
	# Decrement the count of each keyword by 1 every day
	# This will ensure that keywords that are mentioned many times in a given day
	# will remain in the database for a few days to show their importance.
	persons = conn.hgetall('persons')
	for k in persons.keys():
		conn.hincrby('persons', k, -1)
	organizations = conn.hgetall('organizations')
	for k in organizations.keys():
		conn.hincrby('organizations', k, -1)
	glocations = conn.hgetall('glocations')
	for k in glocations.keys():
		conn.hincrby('glocations', k, -1)
	subject = conn.hgetall('subject')
	for k in subject.keys():
		conn.hincrby('subject', k, -1)

	# Sleep for a day and then decrement again
	time.sleep(TTL)