# NY Times API Analysis

**Dependencies:**

1. To install redis

	`brew install redis`
2. To install word cloud library on Mac OS X

  `pip install -U pytagcloud`
  
  `brew install homebrew/python/pygame`
3. To install textblob for sentiment analysis

   `pip install -U textblob`
   
	 `python -m textblob.download_corpora`

**Running the service locally:**

1. Start the Redis server
	* `redis-server`
	
2. Enter today's article data into redit and create word clouds. Images will be saved to .png files in nytimes/lib directory.
	* `cd <path to project>; python nytimes/lib/articles.py`
	
3. Begin removing stale article data
	* `python nytimes/lib/delete_stale_data.py`
	
4. Begin decrementing keyword counts
	* `python nytimes/lib/decrement_topic_counts.py`
	
5. Start tracking the moving averages for sentiment analysis
	* `python nytimes/lib/moving_avg.py`
	
6. Start the API
	* `python nytimes/bin/nyt_homeless_api.py.py`
	
**Hitting the API:**

1. Get organizations keywords (other types: persons, glocations, subjects)
 * `curl localhost:5000/keywords?type=organizations`
 
2. Get average sentiment (other type: movingAvgArticleSubjectivity)
 * `curl localhost:5000/avg_sentiment?type=movingAvgArticlePolarity`
 
3. Get most positive article of the day
 * `curl localhost:5000/positive_article`
 
4. Get most negative article of the day
 * `curl localhost:5000/negative_article`
