# Storytelling-Final-Project

**Dependencies:**

1. To install the required python packages:
	`pip install -r requirements.txt`
2. Services: Redis and ngrok
	`brew install redis ngrok`

**Running the service locally:**

1. Start the Redis server
	`redis-server`
2. Start the text message API
	`cd <path to project>; python lib/alert_api.py`
3. Expose the local flask server so Twilio can reach it
	`ngrok http 80`
3. Configure Twilio
	Note: this requires the number to be live and have Avi's Twilio credentials
	
	* On twilio.com, navigate to the "manage numbers" page

