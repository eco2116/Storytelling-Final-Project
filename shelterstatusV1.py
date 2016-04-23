from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy import AppAuthHandler
from tweepy import Cursor
from pymysql import Error
import pymysql
import re
import time
import datetime

def insert(cur,data):
    """Insert a record"""
    sql = "INSERT INTO Shelter VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
    try:
        # print ("%s,%s",(sql, params))
        cur.execute(sql)
        conn.commit() # pymysql does not autocommit
    except pymysql.Error as e:
        print(e)

def process_tweet(text):
    for (pattern, repl) in patterns: 
        text = re.sub(pattern, repl, text)
    return text


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

auth = AppAuthHandler(ckey, csecret)
api = API(auth)

conn = pymysql.connect(db='bigdata', host='', port=3306,user='',passwd='',use_unicode=True, charset='utf8')
cur = conn.cursor()

replacement_patterns = [ (r'@\S*',''),(r'#\S*',''),(r'rt\S*','')]
patterns = [(re.compile(pattern), repl) for (pattern, repl) in replacement_patterns]

sql = 'select max(date) from Shelter'
cur.execute(sql)
lasttime=cur.fetchone()[0]
if lasttime==None:
    lasttime = datetime.datetime(2016, 4, 5, 18, 00)
searchterms=['ckspyy']

print lasttime
for eachsearch in searchterms:
    print(eachsearch)
    for tweets in Cursor(api.search, q=eachsearch,lang="en",count=100).pages(30):
        for subtweet in tweets:
            try:
                # print subtweet.created_at
                # print lasttime
                # print lasttime>subtweet.created_at
                if (lasttime<subtweet.created_at):
                    content=subtweet.text.lower()
                    content=process_tweet(content)
                    content=content.split(',')
                    print content
                    data=[subtweet.created_at,content[0],content[1],content[2],content[3],subtweet.id_str,content[4],content[5]]
                    insert(cur,data)
            except Error as e:
                print(e)

cur.close()
conn.close()







