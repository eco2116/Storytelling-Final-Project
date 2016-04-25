# $ pip install -U textblob
# $ python -m textblob.download_corpora

import urllib2
import json
from textblob import TextBlob
import operator

nyt_endpoint = "http://api.nytimes.com/svc/"
search = "search/v2/articlesearch.json"
comments = "community/v3/user-content/url.json"
search_term = "homeless"
api_key = ""
community_key = ""

url = nyt_endpoint + search + "?q=" + search_term + "&api-key=" + api_key + \
	"&begin_date=20160101&end_date=20160425"

abstract_dict = {}
keywords_dict = {}
subj_dict = {}
org_dict = {}
geo_dict = {}
persons_dict = {}

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
	# 10 responses per page, plus partial page
	return json_response["meta"]["hits"] / 10 + 1

def analyze_page(page_no):
	response = get_article_page(page_no)
	json_response = json.loads(response)["response"]
	#print json.dumps(json_response)
	hits = json_response["meta"]["hits"]
	# print "hits: " + str(hits)
	docs = json_response["docs"]

	for doc in docs:
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
					increment_dict(subj_dict, val)
				elif name == "organizations":
					increment_dict(org_dict, val)
				elif name == "glocations":
					increment_dict(geo_dict, val)
				elif name == "persons":
					increment_dict(persons_dict, val)

	sentiment_dict = dict()
	for v in abstract_dict.values():
		abstract_blob = TextBlob(v)
		sentiment_dict[v] = abstract_blob.sentiment

pages = total_pages()
print pages
for i in range(0,2):
	analyze_page(i)

#print json.dumps(geo_dict)
#print subj_dict

sorted_geos = sorted(geo_dict.items(), key=operator.itemgetter(1))
print sorted_geos
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
