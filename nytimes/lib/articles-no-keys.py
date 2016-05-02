# $ pip install -U textblob
# $ python -m textblob.download_corpora

import urllib2
import json
import time
from textblob import TextBlob
import operator
import redis
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

nyt_endpoint = "http://api.nytimes.com/svc/"
search = "search/v2/articlesearch.json"
comments = "community/v3/user-content/url.json"
search_term = "homeless+new+york+city"
api_key = "a4a0aa37b8be0427990cd17ee20ea846:6:74332406"
community_key = "5c55d179c8f553939c5d16f926fee4e0:5:74332406"

conn = redis.Redis()

url = nyt_endpoint + search + "?q=" + search_term + "&api-key=" + api_key + \
	"&begin_date=20160401&end_date=20160425"

abstract_dict = {}
keywords_dict = {}
subj_dict = {}
org_dict = {}
geo_dict = {}
persons_dict = {}
sentiment_dict = {}

def get_article_page(page):
	return urllib2.urlopen(url + "&page=" + str(page)).read()

def increment_dict(incr_dict, key):
	try:
		incr_dict[key] = incr_dict[key] + 1
	except KeyError:
		incr_dict[key] = 1

def total_pages():
	response = get_article_page(0)
	json_response = json.loads(response)["response"]
	#print json.dumps(json_response)
	# 10 responses per page, plus partial page
	return json_response["meta"]["hits"] / 10 + 1

def analyze_page(page_no):
	response = get_article_page(page_no)
	json_response = json.loads(response)["response"]
	#print json.dumps(json_response)
	hits = json_response["meta"]["hits"]
	# print "hits: " + str(hits)
	docs = json_response["docs"]

	article_count = 0

	for doc in docs:

		#make sure we have hte requisite fields 
		if doc["pub_date"] and doc['abstract'] and doc['web_url']:
			text_blob = TextBlob(doc['abstract'])
			sentiment = text_blob.sentiment

			article_field_map = {
				'title' : doc['web_url'],
				'polarity' : sentiment.polarity,
				'subjectivity' : sentiment.subjectivity,
				'pub_date' : doc['pub_date']
			}		
					
			conn.hmset(time.time(), article_field_map)

		url = doc["web_url"]
		if url:
			abstract = doc["abstract"]
			if abstract:
				abstract_dict[url] = abstract

			keywords = doc["keywords"]
			for keyword in keywords:
				val = keyword["value"]
				name = keyword["name"]

				#subject, organizations, glocations, persons
				if name == "subject":
					conn.hincrby('subject', val)
				elif name == "organizations":
					conn.hincrby('organizations', val)
				elif name == "glocations":
					increment_dict(geo_dict, val)
					conn.hincrby('glocations', val)
				elif name == "persons":
					conn.hincrby('persons', val)

	# for v in abstract_dict.values():
	# 	abstract_blob = TextBlob(v)
	# 	sentiment_dict[v] = abstract_blob.sentiment

#pip install -U pytagcloud
#brew install homebrew/python/pygame
def generate_word_cloud(counts):
	tags = make_tags(counts.items(), maxsize=100)
	create_tag_image(tags, 'cloud_large.png', size=(900, 600), fontname='Lobster')

#print json.dumps(geo_dict)
#print subj_dict
if __name__ == "__main__":
	pages = total_pages()
	print pages
	for i in range(0,5):
		analyze_page(i)

	generate_word_cloud(geo_dict)

# all_comment_text = ""
# for url in abstract_dict.keys():
# 	# Returns most recent 25 comments
# 	print url
# 	response = urllib2.urlopen(nyt_endpoint + comments + "?api-key=" + community_key + "&url=" + url).read()
# 	print response

# 	try: 
# 		json_response = json.loads(response)["response"]
# 		comments = json_response["comments"]
		
# 		for comment in comments:
# 			all_comment_text += comment["commentBody"]
# 	except KeyError:
# 		continue

# print all_comment_text
# print sentiment_dict
# print keywords_dict
# for v in abstract_dict.values():
# 	print v
