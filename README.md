# Storytelling-Final-Project

## Text Message Service

**Dependencies:**

1. To install the required python packages:
	`pip install -r requirements.txt`
2. Services: Redis and ngrok
	`brew install redis ngrok`

**Running the service locally:**

1. Start the Redis server
	* `redis-server`
2. Start the text message API
	`* cd <path to project>; python lib/alert_api.py`
3. Expose the local flask server so Twilio can reach it
	* `ngrok http 80`
3. Configure Twilio
	(Note: this requires the number to be live and have Avi's Twilio credentials)
	* On twilio.com, navigate to the "manage numbers" page
	* Click the number "(251) 333-5913"
	* Under the "Messaging" header create a new TwiML App
	* Under "Messaging" header copy and paste the url outputted by ngrok. This will be in the form of: 
	`Forwarding                    <url> -> localhost:80`

**Testing the service**

1. Publishing to a resource queue
	* Text in the format `<channel name>, <name of donator>, <address>`
2. Subscribing to a resource queue
	* Text in the formart `subscribe <channel name>, <phone number>`

## NY Times API Analysis

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


## Twitter Platform

The "Shelterstatus.py" can be run on a server to process info updates from twitter and update it into an Amazon AWS RDS database everyhour. Withou some validation and error checking, it is able to process and update tweets satisfying certain format requirments.

#Sample msg format
column name: latitude, 	Longitude,	shelter info,	food info,	msid,	                 lan class,	    weather

sample msg:  40.8072,    -73.9488,   yes,   	       yes, 	    720970246908219000.00,	eng wed 3pm, 	rainy



It also checks for the total amount of tweet updates received everyday(rate) and a warnning would be produced if there's too few tweet updates on shelter status by the end of each day.

The shelter status data in the database will be later used for visualiztion on the website to provide homeless people latest shelter statuses in NYC
 

# Webpage

This file will briefly introduce the webpage section for the storytelling final project. This file contains
4 parts, which are Getting Started, User Guidance, Built With, and License.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes
or seeing the project on our website online. See deployment for notes on how to deploy the project on a live system or visit the website.

### Running on Our Website (Recommend)

We recommend you visit our website [Homeless-Story](http://homeless-story.com/) to see our storytelling final project, the fantastic stories we explored, and 
the comprehensive solutions we provided, because of the following reasons:
* Have a unforgettable and touched memory with our real time big data analytics and visualization
* No worries about the credential tokens, easy and smoothly experience our stories
* Get in touch with us, submit your information and help the homeless people with us shoulder by shoulder

### Running the Website Locally

<ol>
<li>Prerequisites</li>
<ul>
<li>Apply for the AWS RDS database credential token</li>
<li>Apply for the Tableau Server credential token</li>
<li>Download the folder and fill in the credential token</li>
<li>High speed Internet access</li>
<li>Browser (Recommend Google Chrome)</li>
</ul>
<li>Running the website</li>
<ul>
<li>Download the and unzip the folder, double check all the six html files are in the same path</li>
<li>Double click the files, and the website should start running</li>
</ul>
</ol>

## User Guidance of the Website

This section will detailed explain every page and give you an overview about the stories we want to tell. 

### Home Page

In this page, you will first see the reported number of the homeless spotted in NYC by today in year 2016. 
This is a real time data analytics based on the 311 database provided by NYC Open Data. 

Scroll down, you will see a visualization about the number of homeless people on the street reported from 2010. You can play with the
visualization to explore more, such as the growing trends, the migration and etc. by simply clicking the year or the 
location or both as a filter, then the visualization map on the left , and the year map on the upper right will start
to change and show the real time analytics and visualization results based on your customized filter.  

When you move your mouse across the visualization, you can see the detailed information, such as the total number of homeless
people or the geolocation. For the year map, the larger the circle is, the more homeless people it has for a specific year and location.

Clicking "Behind the Statistic Button" will lead you to our Background page.

### Background Page

In this page, we listed two mainly reasons that more and more people become homeless and live on the street. 
We interviewed several experts and searched tons of news reports. We found because of the high housing rent and 
lack of centralized source of resources for combatting homelessness, some of college students become homeless people 
after the graduation, even homeless people don't want to go to the shelters.

We also found because of some of the shelters may involve mental illness patient, it becomes unsafe to live in the shelters.
For more detailed stories we explored, please click on the Interview Page.

### Interview Page

In this page, we listed three experts who's willing to accept our interviews and told us more stories behind the statistics.
They shared their experiences and opinions, which motivated us to set up a platform to centralized source of resources for combatting homelessness.

### Solution Page

In this page, we provide a plotform that shelters can use tweet us information about themselves. Information can be food information,
space availability information, course or program availability information, weather information and etc.. We store all these information 
on Amazon AWS RDS, and use Tableau to visualize it. We try to provide a platform that volunteers know the current needs about the 
shelters, and homeless people know where to find their needs and resources.

### Contact Page

We clearly know that our strength is too small, and our resources is not wide enough. However, we have warm-hearted people from the society.
So if people know some external information, or people want to report something, he or she can leave us a message, we can reach out.
Hopefully by doing this, our platform can become more powerful and comprehensive, help to reallocation of resources, and surviving more people.

### About Us Page

We are a excellent and professional team. We are risk taker, passionate, doer and solution thinker. 

## Built With

* Amazon AWS RDS
* Tableau
* JavaScript
* HTML

## License

This project is licensed under the Columbia University License

