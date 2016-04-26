import redis
import time

conn = redis.Redis()

# run daily
while 1:
	persons = conn.hgetall('persons')
	for k in persons.keys():
		conn.hincrby('persons', k, -1)
	print persons
	time.sleep(10)