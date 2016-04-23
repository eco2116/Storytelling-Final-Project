from flask import Flask, request, redirect
import redis
import time
import usaddress
import json
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

	food_alert_dict = {}
	food_alert_dict['zip'] = request.form['FromZip']

	if(request.form['Body']):
		body_info = parse_message(request.form['Body'])
		food_alert_dict['establishment'] = body_info[0]
		food_alert_dict['location'] = body_info[1]

	conn.publish('food', json.dumps(food_alert_dict))

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