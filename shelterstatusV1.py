
# this python code retrieves target tweets on NYC shelter information and process the data to be stored in a Amazon AWS RDS database
# the data in the database will be later used for visualiztion on the website to provide homeless people latest shelter statuses in NYC
# it runs a server using a while loop to execute code block every hour

# import tweepy and pymysql moduel for twitter api and database api connection
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy import AppAuthHandler
from tweepy import Cursor
from pymysql import Error
import pymysql
# import other modules for the purpose this program
import re
import time
import datetime

# program to insert each shelter status update tweet into the database.
def insert(cur,data):
    """Insert a record"""
    sql = "INSERT INTO Shelter VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
    try:
        # print ("%s,%s",(sql, params))
        cur.execute(sql)
        conn.commit() # pymysql does not autocommit
    # print an error message whenever a erroneous tweet is caught
    except pymysql.Error as e:
        print(e)


# pre process the tweet text to extract useful content only
def process_tweet(text):
    for (pattern, repl) in patterns: 
        text = re.sub(pattern, repl, text)
    return text


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""


# combine the authentification info together for later operations
auth = AppAuthHandler(ckey, csecret)
api = API(auth)

# connect to the database 
conn = pymysql.connect(db='bigdata', host='', port=3306,user='',passwd='',use_unicode=True, charset='utf8')
# operator to communicate with the database
cur = conn.cursor()

# basic tweet message processing to get rid of non relavant info
replacement_patterns = [ (r'@\S*',''),(r'#\S*',''),(r'rt\S*','')]
patterns = [(re.compile(pattern), repl) for (pattern, repl) in replacement_patterns]


# timestamp check to make sure only shelter status update appearing later than the last status update time is retrieved and processed.
# the latest update time is store in variable 'lasttime'
sql = 'select max(date) from Shelter'
cur.execute(sql)
lasttime=cur.fetchone()[0]

# in case there's nothing in the database
if lasttime==None:
    lasttime = datetime.datetime(2016, 5, 1, 18, 00)

# the keyword/ secret code for the tweet to be recognized.
searchterms=['ckspyy']

print lasttime

# the while loop finish one loop every hour, doing tweet search , update into database and rate check.
while True:
    # the code block to actually rerieve tweets and preprocess the tweets and insert it into the database
    for eachsearch in searchterms:
        print(eachsearch)
        # the line below search twitter system for target tweets
        for tweets in Cursor(api.search, q=eachsearch,lang="en",count=100).pages(30):
            for subtweet in tweets:
                try:
                    # print subtweet.created_at
                    # print lasttime
                    # print lasttime>subtweet.created_at

                    #  check if the tweet should be checked for updates.
                    if (lasttime<subtweet.created_at):
                        # convert everything into lowercase
                        content=subtweet.text.lower()
                        # pre process the tweet before inserting to database
                        content=process_tweet(content)
                        # split the tweet into respective fields
                        content=content.split(',')
                        # to print out the tweet updated into database
                        print content
                        # format the update msg into the format matching that in the database
                        data=[subtweet.created_at,content[0],content[1],content[2],content[3],subtweet.id_str,content[4],content[5]]
                        # insert the msg into database
                        insert(cur,data)
                except Error as e:
                    print(e)
    # the tweet search and update happens everyhour.
    time.sleep(3600)

    # check the daily rates
    # firstly, find the current year, month, day
    dailymonitor=str(datetime.datetime.now()).split(' ')[0]
    year  = dailymonitor.split('-')[0]
    month = dailymonitor.split('-')[1]
    day   = dailymonitor.split('-')[2]
    # build the sql command to check how many tweets have been inserted into the database today.
    dailymonitor = datetime.datetime(year, month, day, 00, 00, 0 )
    checktime = datetime.datetime(year, month, day, 23, 00, 0 )

    #  if current time is in the last hour of each day, trigger one round of rate check
    if datetime.datetime.now()>checktime:
        sql = "select count(*) from Shelter where date>%s" %(dailymonitor)
        cur.execute(sql)
        # find the current rate today
        rate=cur.fetchone()[0]
        # if the rates drop below a certain limit, alarm the staff as shown below
        if rate <100:
            print 'warning! the tweet updates are slow, investigation is suggested'


cur.close()
conn.close()















