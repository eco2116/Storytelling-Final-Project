from flask import Flask, request, jsonify
import redis
# import collections
import json

app = Flask(__name__)
conn = redis.Redis()

@app.route("/keywords", methods=['GET'])
def get_distribution():
	key_word_type = request.args.get('type')
	data = conn.hgetall(key_word_type)
	return jsonify(data)

@app.route("/avg_sentiment", methods=['GET'])
def get_moving_avg():
	sentiment_type = request.args.get('type')
	if sentiment_type == 'polarity':
		avg = conn.get('movingAvgArticlePolarity')
	elif sentiment_type == 'subjectivity':
		avg = conn.get('movingAvgArticleSubjectivity')
	return jsonify({'moving_avg' : avg})


if __name__ == "__main__":
    app.debug = True
    app.run()