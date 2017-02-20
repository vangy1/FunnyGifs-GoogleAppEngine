# Import libraries
import MySQLdb
import os
import json
import webapp2
# -----------------

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        subreddit = self.request.get('vertical', "funny")
        before = self.request.get('before', 100000000)  # GET before value from url
        size = self.request.get('size', 5)  # GET size value from url

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

        sql = "SELECT id,url,title,UNIX_TIMESTAMP(timestamp),reddit_id FROM archive WHERE subreddit='%s' AND id < '%d' AND url like '%%.gifv' group by reddit_id ORDER BY id DESC limit %d" % (subreddit,int(before),int(size))
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            self.response("Error 51")
        objectList = []
        for row in result:
            jsonObject = Object()
            jsonObject.id = row[0]
            jsonObject.url = str(row[1]).replace("gifv", "mp4").replace("gif", "mp4")
            jsonObject.placeholder = str(row[1]).replace(".gifv", "h.jpg").replace(".gif", "h.jpg")
            jsonObject.title = row[2]
            jsonObject.timestamp = str(row[3])
            jsonObject.reddit_id = row[4]
            objectList.append(jsonObject)

        # --------------- Print as valid JSON ---------------
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['access-control-allow-origin'] = '*'
        self.response.write("[")
        i = 0
        length = len(objectList)
        while i < length - 1:
            self.response.write(objectList[i].to_JSON() + ",\n")
            i += 1
        self.response.write(objectList[length - 1].to_JSON())
        self.response.write("]")
        # ---------------------------------------------------
        cursor.close()
        db.close()

app = webapp2.WSGIApplication([
    ('/getposts_web_client', MainHandler)
], debug=True)
