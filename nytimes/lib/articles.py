# Import required python libraries
import urllib2 # for calling NYTimes endpoint
import json # for handling JSON
import time # 
import redis # for storing data / sliding window
from textblob import TextBlob # for sentiment analysis
import operator # for sorting

# Libraries for creating word clouds
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud import create_tag_image, create_html_data, make_tags, LAYOUT_HORIZONTAL, \
	LAYOUTS, LAYOUT_MIX, LAYOUT_VERTICAL, LAYOUT_MOST_HORIZONTAL, LAYOUT_MOST_VERTICAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts

# Endpoints and search terms for NY Times articles
nyt_endpoint = "http://api.nytimes.com/svc/"
search = "search/v2/articlesearch.json"
search_term = "homeless+new+york+city"

# API key - excluded from github for privacy; contact our group
# or create a free one on NYTimes if needed for testing purposes
api_key = ""

# Redis connection
conn = redis.Redis()

# Get time format that NYTimes can parse for date range/sampling window of 1 day
today = int(time.strftime("%Y%m%d"))
yesterday = today - 1

# Format NYT endpoint
url = nyt_endpoint + search + "?q=" + search_term + "&api-key=" + api_key + \
	"&begin_date=" + str(yesterday) + "&end_date=" + str(today)

# Initialize dictionaries to store keywords, abstracts, and sentiments
abstract_dict = {}
keywords_dict = {}
subj_dict = {}
org_dict = {}
geo_dict = {}
persons_dict = {}
sentiment_dict = {}

# Get response from NYTimes
def get_article_page(page):
	# Choose the page number of the results to return
	return urllib2.urlopen(url + "&page=" + str(page)).read()

def increment_dict(incr_dict, key):
	# If key exists, increment by 1. If not, initialize to 1.
	try:
		incr_dict[key] = incr_dict[key] + 1
	except KeyError:
		incr_dict[key] = 1

# Determine the total number of pages returned by the search
def total_pages():
	response = get_article_page(0)
	json_response = json.loads(response)["response"]
	print json.dumps(json_response)
	# 10 responses per page, plus partial page
	return json_response["meta"]["hits"] / 10 + 1

# Analyze a single NYTimes result page
def analyze_page(page_no):

	# Load in relevant blocks from the returned JSON
	response = get_article_page(page_no)
	json_response = json.loads(response)["response"]
	hits = json_response["meta"]["hits"]
	docs = json_response["docs"]
	article_count = 0

	# Iterate through all documents (articles)
	for doc in docs:

		# To install textblob dependency:
		# pip install -U textblob
		# python -m textblob.download_corpora
		#
		# make sure we have the required fields 
		if doc["pub_date"] and doc['abstract'] and doc['web_url']:
			text_blob = TextBlob(doc['abstract'])
			sentiment = text_blob.sentiment

			# Use hash in reddit to store sentiment data
			article_field_map = {
				'title' : doc['web_url'],
				'polarity' : sentiment.polarity,
				'subjectivity' : sentiment.subjectivity,
				'pub_date' : doc['pub_date']
			}		
				
			# Store hash based on time	
			conn.hmset(time.time(), article_field_map)

		# Classify keywords of each article
		url = doc["web_url"]
		if url:
			abstract = doc["abstract"]
			if abstract:
				abstract_dict[url] = abstract

			keywords = doc["keywords"]
			for keyword in keywords:
				val = keyword["value"]
				name = keyword["name"]

				# Keyword types returned by NYTimes:
				# subject, organizations, glocations, persons
				if name == "subject":
					# Increment the dictionary for world clouds
					increment_dict(subj_dict, val)
					# Increment reddit record for that specific keyword
					# redis can handle initializing the key for first occurrence
					conn.hincrby('subject', val)
				elif name == "organizations":
					increment_dict(org_dict, val)
					conn.hincrby('organizations', val)
				elif name == "glocations":
					increment_dict(geo_dict, val)
					conn.hincrby('glocations', val)
				elif name == "persons":
					increment_dict(persons_dict, val)
					conn.hincrby('persons', val)

# Generate word clouds given a dictionary of frequency of keywords
#
# To install dependencies on Mac OS X:
# pip install -U pytagcloud
# brew install homebrew/python/pygame
def generate_word_cloud(counts, title):
	# Sort the keywords
	sorted_wordscount = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]
	
	# Generate the word cloud image
	create_tag_image(make_tags(sorted_wordscount, minsize=50, maxsize=150), title + '.png', size=(1300,1150), 
		background=(0, 0, 0, 255), layout=LAYOUT_MIX, fontname='Molengo', rectangular=True)

if __name__ == "__main__":
	# Analyze all pages returned by NYTimes
	pages = total_pages()
	print pages
	for i in range(0,pages):
		analyze_page(i)
	
	# Generate and save word cloud images locally for each type of keyword
	generate_word_cloud(subj_dict, 'subjects')
	generate_word_cloud(org_dict, 'organizations')
	generate_word_cloud(persons_dict, 'persons')
	generate_word_cloud(geo_dict, 'glocations')

