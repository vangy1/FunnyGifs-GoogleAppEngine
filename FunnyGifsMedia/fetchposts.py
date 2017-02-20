# Import libraries
import sys
sys.path.insert(0, 'libs')
import MySQLdb
import json
import time
from google.appengine.api import urlfetch
import os
import webapp2
# -----------------

class Fetcher:
    def __init__(self, subreddits, numOfRequests):
        self.subreddits = subreddits
        self.numOfRequests = numOfRequests

        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            self.db = MySQLdb.connect(
                unix_socket='/cloudsql/funny-gifs:us-central1:funny-gifs',
                user='root',
                passwd='37126094',
                db='funnynewtab'
            )
        else:
            self.db = MySQLdb.connect("104.155.149.131", "root", "37126094", "funnynewtab")
        self.cursor = self.db.cursor()

    def startFetch(self):
        for subreddit in self.subreddits:
            self.currentSubreddit = subreddit
            self.fetchPostsFromSubreddit()

    def fetchPostsFromSubreddit(self):
        posts = []
        after = ""
        for i in range(0, self.numOfRequests):
            result = ""
            url = "https://www.reddit.com/r/%s/.json?limit=%d&after=%s" % (self.currentSubreddit, 100, after)
            for x in range(0, 4):  # try 4 times
                try:
                    result = urlfetch.fetch(url=url,deadline=60, headers={'User-agent': 'funny gifs'})
                    str_error = None
                except Exception as str_error:
                    pass
                if str_error:
                    time.sleep(0)  # wait for 2 seconds before trying to fetch the data again
                else:
                    break
            responseJson = json.loads(result.content)
            after = str(responseJson['data']['after'])
            newPosts = responseJson['data']['children']
            for post in range(0, len(newPosts)):
                posts.append(newPosts[post])
        posts = self.filterPosts(posts)
        self.addPostsToDatabase(posts)

    def filterPosts(self, posts):
        filteredPosts = []
        for post in range(0, len(posts)):
            url = posts[post]['data']['url'].encode('ascii', 'ignore').decode('ascii')
            title = posts[post]['data']['title'].encode('ascii', 'ignore').decode('ascii')
            nsfw = posts[post]['data']['over_18']
            stickie = posts[post]['data']['stickied']
            permalink = posts[post]['data']['permalink'].encode('ascii', 'ignore').decode('ascii')
            name = posts[post]['data']['name'].encode('ascii', 'ignore').decode('ascii')
            if nsfw != "true" and stickie != "1" and str(url).find("i.imgur") != -1 and str(url).find(".gif") != -1:
                filteredPost = type('lamdbaobject', (object,), {})()
                filteredPost.url = url
                filteredPost.title = title
                filteredPost.permalink = permalink
                filteredPost.reddit_id = name
                filteredPosts.append(filteredPost)
        return filteredPosts

    def addPostsToDatabase(self, posts):
        posts = self.removeDuplicatePosts(posts)
        for post in range(0, len(posts)):
            title = MySQLdb.escape_string(posts[post].title.decode("utf-8"))
            url = posts[post].url
            permalink = posts[post].permalink
            reddit_id = posts[post].reddit_id

            sql = "INSERT INTO archive (url,title,permalink,reddit_id,subreddit) VALUES ('%s','%s','%s','%s','%s')" % (
                url, title, permalink, reddit_id, self.currentSubreddit)
            self.cursor.execute(sql)
            self.db.commit()

    def removeDuplicatePosts(self, posts):
        # Query for recent posts to check against so duplicate posts won't be inserted
        sql = "SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'"
        self.cursor.execute(sql)
        sql = "SELECT reddit_id FROM archive WHERE subreddit='%s' ORDER BY timestamp DESC limit 1500" % (
        self.currentSubreddit)
        self.cursor.execute(sql)
        recentPostsSQLRows = self.cursor.fetchall()
        # ----------------------

        recentPosts = []
        for row in recentPostsSQLRows:
            recentPosts.append(str(row[0]))

        postsToInsert = []
        for post in range(0, len(posts)):
            reddit_id = posts[post].reddit_id
            duplicateFound = False
            for i in range(0, len(recentPosts)):
                if str(reddit_id) == str(recentPosts[i]):
                    duplicateFound = True
            if duplicateFound == False:
                postsToInsert.append(posts[post])
        return postsToInsert

    # Close database connection after object is destroyed
    def __del__(self):
        self.db.close()
        self.cursor.close()


# Google App engine
class MainHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        # Specify subreddits to fetch from
        subreddits = ["funny", "animegifs", "NatureGifs", "kittengifs"]
        # Specify number of requests to be performed for each subreddit
        numOfRequests = 5
        fetchClass = Fetcher(subreddits,numOfRequests)
        fetchClass.startFetch()
        self.response.write("Finished !")

app = webapp2.WSGIApplication([
    ('/fetchposts', MainHandler)
], debug=True)
