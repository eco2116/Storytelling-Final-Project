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

@app.route("/positive_article", methods=['GET'])
def get_positive_article():
	max_val = -1.0
	positive_article = ""
	keys = conn.keys()
	for key in keys:
		try:
			pos = conn.hget(key, 'polarity')
			if float(pos) > float(max_val):
				max_val = pos
				positive_article = conn.hget(key, 'title')

		except Exception:
			continue
	print max_val
	return positive_article

@app.route("/negative_article", methods=['GET'])
def get_negative_article():
	min_val = 1.0
	negative_article = ""
	keys = conn.keys()
	for key in keys:
		neg = conn.hget(key, 'polarity')

		if neg:
			print "neg" + str(neg)
			if float(neg) < float(min_val):
				min_val = neg
				negative_article = conn.hget(key, 'title')

	print min_val
	return negative_article

if __name__ == "__main__":
    app.debug = True
    app.run()

    # Using this will allow it to be accessed from the outside world
    # app.run('0.0.0.0')

