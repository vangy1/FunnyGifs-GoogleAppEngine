# Import libraries
import MySQLdb
import os
import json
import webapp2
# -----------------

# Object for saving JSON values
class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

# Google App engine
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # --------------- Database Connection ---------------
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

        sql = "SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'"
        cursor.execute(sql)

        sql = "SELECT archive.id, posts.url, posts.title, posts.permalink, posts.reddit_id, posts.timestamp FROM posts JOIN archive ON (posts.reddit_id = archive.reddit_id)"
        cursor.execute(sql)
        result = cursor.fetchall()

        posts = []
        for row in result:
            jsonObject = Object()
            jsonObject.recency = "fresh"
            jsonObject.id = row[0]
            jsonObject.url = row[1]
            jsonObject.title = row[2]
            jsonObject.permalink = row[3]
            jsonObject.reddit_id = row[4]
            jsonObject.timestamp = str(row[5])
            posts.append(jsonObject)


        sql = "SELECT * FROM archive WHERE timestamp between DATE_SUB(NOW(), INTERVAL 41 DAY) and DATE_SUB(NOW(), INTERVAL 21 DAY) order by RAND() limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            jsonObject = Object()
            jsonObject.recency = "older"
            jsonObject.id = row[0]
            jsonObject.url = row[1]
            jsonObject.title = row[2]
            jsonObject.permalink = row[3]
            jsonObject.reddit_id = row[4]
            jsonObject.timestamp = str(row[5])
            posts.append(jsonObject)

        # --------------- Print as valid JSON ---------------
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['access-control-allow-origin'] = '*'
        self.response.write("[")
        i = 0
        length = len(posts)
        while i < length - 1:
            self.response.write(posts[i].to_JSON() + ",\n")
            i += 1
        self.response.write(posts[length - 1].to_JSON())
        self.response.write("]")
        # ---------------------------------------------------

        cursor.close()
        db.close()

app = webapp2.WSGIApplication([
    ('/getposts_chrome', MainHandler)
], debug=True)
