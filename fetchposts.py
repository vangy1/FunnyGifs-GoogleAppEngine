# Import libraries
import sys
sys.path.insert(0, 'libs')
import MySQLdb
import requests
import os
import webapp2
# -----------------

db = None
cursor = None
howmany = 5
z = 1
posts = []


def doMultipleRedditRequests(after):
    if z <= howmany:
        if after == "":
            getListing("funny", 100, "")
        else:
            getListing("funny", 100, after)
    else:
        processData()

def processData():
    filtered_posts = []
    global posts

    for post in range(0,len(posts)):
        url = posts[post]['data']['url']
        title = posts[post]['data']['title']
        nsfw = posts[post]['data']['over_18']
        stickie = posts[post]['data']['stickied']
        permalink = posts[post]['data']['permalink']
        name = posts[post]['data']['name']
        if nsfw != "true" and stickie != "1" and str(url).find("i.imgur") != -1 and str(url).find(".gif") != -1:
            o = type('lamdbaobject', (object,), {})()
            o.url = url
            o.title = title
            o.permalink = permalink
            o.reddit_id = name
            filtered_posts.append(o)
    writeToDb(filtered_posts)


def addToOtherResponses(response):
    newPosts = response['data']['children']
    for post in range(0,len(newPosts)):
        posts.append(newPosts[post])


def getListing(subreddit, limit, after):
    url_listing = "https://www.reddit.com/r/%s/.json?limit=%d&after=%s" % (subreddit,limit,after)
    return runCurl(url_listing)


def runCurl(url):
    global z

    r = requests.get(url, headers = {'User-agent': 'funny gifs'})
    response = r.json()

    z += 1

    after = str(response['data']['after'])
    addToOtherResponses(response)
    doMultipleRedditRequests(after)


def writeToDb(filteredPosts):
    if len(filteredPosts) > 0:
        sql = "TRUNCATE table posts"
        cursor.execute(sql)

    sql = "SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'"
    cursor.execute(sql)

    for post in range(0,len(filteredPosts)):
        title = MySQLdb.escape_string(filteredPosts[post].title)
        url = filteredPosts[post].url
        permalink = filteredPosts[post].permalink
        reddit_id = filteredPosts[post].reddit_id
        sql = "INSERT INTO posts (url,title,permalink,reddit_id) VALUES ('%s','%s','%s','%s')" % (url,title,permalink,reddit_id)
        cursor.execute(sql)

    addNewPostsToArchive(filteredPosts)


def addNewPostsToArchive(filteredPosts):
    sql = "SELECT reddit_id from archive group by 1 ORDER BY timestamp DESC limit 300"
    cursor.execute(sql)
    result = cursor.fetchall()

    existingPosts = []
    for row in result:
        existingPosts.append(str(row[0]))

    dedupedNewPosts = []
    for post in range(0, len(filteredPosts)):
        reddit_id = filteredPosts[post].reddit_id
        dupFound = 0
        for i in range(0, len(existingPosts)):
            if str(reddit_id) == str(existingPosts[i]):
                dupFound = 1
        if dupFound == 0:
            dedupedNewPosts.append(filteredPosts[post])

    alreadyInsertedUrls = []
    for post in range(0,len(dedupedNewPosts)):
        url = dedupedNewPosts[post].url
        if url not in alreadyInsertedUrls: # Check if url of deduptedPosts isn't in array of Urls that were already inserted into the databse
            title = MySQLdb.escape_string(dedupedNewPosts[post].title)
            permalink = dedupedNewPosts[post].permalink
            reddit_id = dedupedNewPosts[post].reddit_id
            sql = "INSERT INTO archive (url,title,permalink,reddit_id) VALUES ('%s','%s','%s','%s')" % (url,title,permalink,reddit_id)
            cursor.execute(sql)
            db.commit()
            alreadyInsertedUrls.append(url)  # Add the url into already inserted urls

# Google App engine
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # --------------- Database Connection ---------------
        global db
        global cursor

        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            db = MySQLdb.connect(
                unix_socket='/cloudsql/funny-gifs:us-central1:funny-gifs',
                user='root',
                passwd='37126094',
                db='funnynewtab'
            )
        else:
            db = MySQLdb.connect("104.155.149.131", "root", "37126094", "funnynewtab")
        cursor = db.cursor()
        # ---------------------------------------------------
        doMultipleRedditRequests("") # Start fetching script

        self.response.write("Finished !")

        db.close()
        cursor.close()

app = webapp2.WSGIApplication([
    ('/fetchposts', MainHandler)
], debug=True)
