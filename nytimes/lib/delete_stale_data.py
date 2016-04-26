import sys
import redis
import time

#set time to live to 10 minutes for the rental events
TTL = 600
conn = redis.Redis()

while True:
	keys = conn.keys()
	current_time = time.time()
	for key in keys:
		try:
			if(current_time - float(key)  > TTL):
				conn.delete(key)
		except ValueError as e:
			#if you come across the "movingAvgRate" key, ignore it
			continue;

	time.sleep(5)
