from flask import Flask, request, redirect
import redis

import twilio.twiml

app = Flask(__name__)
conn = redis.Redis()

@app.route("/", methods=['GET', 'POST'])
def process_food_event():

	food_alert = {}
	resp = twilio.twiml.Response()
	print request.form['Body']
	print request.form['FromCity']
	print request.form['FromZip']
	food_alert


	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)