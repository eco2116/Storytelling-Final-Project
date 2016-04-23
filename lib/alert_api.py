from flask import Flask, request, redirect
import redis
import time
import usaddress

import twilio.twiml

app = Flask(__name__)
conn = redis.Redis()

@app.route("/", methods=['GET', 'POST'])
def process_food_event():
	
	t = time.time()
	resp = twilio.twiml.Response()
	print request.form['Body']
	print request.form['FromCity']
	print request.form['FromZip']

	#commented for testing in Boston
	# if(request.form['FromCity'] != 'New York'):
	# 	resp.message("Sorry, we only process events within NYC!")
	# 	return resp

	if(request.form['Body']):
		body_info = parse_message(request.form['Body'])
		food_alert_dict = {
			'establishment' : body_info['establishment'],
			'location' : body_info['location'],
			'zip' : request.form['FromZip']
		}	

	food_alert_dict = {
		'establishment' : request.form['Body'],
		'zip' : request.form['FromZip']
	}
	conn.hmset(t, food_alert_dict)
	return str(resp)


# @app.route("/subscribe", methods=['GET', 'POST'])
# def subscribe_user():

def parse_message(text):
	"""
	Parses an alert text in the form <establishment name>, <address of any format>
    Parameters:
    	text - the body of the twilio request
    Returns:
    	dict - dictionary with name of establishment and parsed address dictionary

    """
	components = string.split(',')
	return {establishment : components[0], location : usaddress.parse(components[1])}



if __name__ == "__main__":
    app.run(debug=True)