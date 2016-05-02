from flask import Flask, request, redirect
import redis
import time
import usaddress
import json
import twilio.twiml
import string
import threading
import Queue

# Find these values at https://twilio.com/user/account
account_sid = ""
auth_token = ""
client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)
conn = redis.Redis()
#initialize a queue of subscribers for each channel
queueDic = {
    	'food' : Queue.Queue(),
    	'shelter' : Queue.Queue(),
    	'clothing' : Queue.Queue()
    }

#source: https://gist.github.com/jobliz/2596594
class Subscriber(threading.Thread):
	"""
	A subscriber thread that sends a message to a user when a resource becomes available

    """
	def __init__(self, r, channel, phone):
		threading.Thread.__init__(self)
		self.redis = r
		self.pubsub = self.redis.pubsub()
		self.pubsub.subscribe([channel])
		self.phone = phone

	def work(self, item):
		print item
		try:
			info = json.loads(item['data'])
			#fill in the body more when we have users!!!
			message = client.messages.create(to=self.phone, from_="+12513335913",
                                     body="Resource Available")
		except Exception as e:
			return
    
	def run(self):
		for item in self.pubsub.listen():
			self.work(item)

class Master(threading.Thread):
	"""
	A thread to handle each queue of subscribers

    """
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
	  		#get sub thread from queueg
	  		sub = self.queue.get()
	  		sub.start()
	  		self.queue.task_done()


@app.route("/", methods=['GET', 'POST'])
def process_resource():
	"""
	Handles a text message event. This can be a subscribing event or a publishing event 

    """
	t = time.time()
	resp = twilio.twiml.Response()
	print request.form['Body']
	print request.form['FromCity']
	print request.form['FromZip']

	if(request.form['FromCity'] != 'New York'):
		resp.message("Sorry, we only process events within NYC!")
		return resp

	resource_alert_dict = {}
	resource_alert_dict['zip'] = request.form['FromZip']

	if(request.form['Body']):
		body_info = parse_message(request.form['Body'])
		resource_alert_dict['channel'] = body_info['channel']
		if body_info['phone']:
			resource_alert_dict['channel'] = body_info['phone']
			#put the subscriber onto the queue he or she is subscribing to
			client = Subscriber(conn, resource_alert_dict['channel'], resource_alert_dict['phone'])
			queueDic[resource_alert_dict['channel']].put(client)
			return str(resp)

		resource_alert_dict['establishment'] = body_info['establishment']
		resource_alert_dict['location'] = body_info['location']

	conn.publish(resource_alert_dict['channel'], json.dumps(resource_alert_dict))

	return str(resp)


# @app.route("/subscribe", methods=['GET', 'POST'])
# def subscribe_user():

def parse_message(text):
	"""
	Parses an alert text in the form <channel name>, <establishment name>, <address of any format>
    Parameters:
    	text - the body of the twilio request
    Returns:
    	dict - dictionary 

    """
	components = string.split(text, ',')
	if components[0] == 'subscribe':
		return {'phone' : components[1]}

	return {'channel' : components[0],'establishment' : components[1], 'location' : usaddress.parse(components[2])}



if __name__ == "__main__":
    app.run(debug=True)  
    #initialize and start a master thread for each queue
    for q in queueDic:
    	master = Master(q)
    	master.start()



