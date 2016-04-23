import redis
import threading
import json

#source: https://gist.github.com/jobliz/2596594
class Subscriber(threading.Thread):
	def __init__(self, r, channels):
		threading.Thread.__init__(self)
		self.redis = r
		self.pubsub = self.redis.pubsub()
		self.pubsub.subscribe(channels)

	def work(self, item):
		print item
		try:
			info = json.loads(item['data'])
			
		except Exception as e:
			return
    
	def run(self):
		for item in self.pubsub.listen():
			if item['data'] == "KILL":
				self.pubsub.unsubscribe()
				print self, "unsubscribed and finished"
				break
			else:
				self.work(item)


if __name__ == "__main__":
	r = redis.Redis()
	client = Subscriber(r, ['food'])
	client.start()


