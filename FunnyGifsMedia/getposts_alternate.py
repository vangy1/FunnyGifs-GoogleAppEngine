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

        subreddit = self.request.get('vertical', "funny")
        minimum = self.request.get('minimum', 0)  # GET before value from url
        maximum = self.request.get('maximum', 0)  # GET after value from url

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

        sql = "SELECT * FROM (SELECT url,title,id,reddit_id FROM archive WHERE subreddit='%s' AND id > '%d' AND url LIKE '%%.gifv' ORDER BY id ASC LIMIT 2) a UNION ALL SELECT * FROM (SELECT url,title,id,reddit_id FROM archive WHERE subreddit='%s' AND id < '%d' AND url LIKE '%%.gifv' ORDER BY id DESC LIMIT 2) b LIMIT 2" % (
            subreddit, int(maximum), subreddit, int(minimum))
        cursor.execute(sql)
        result = cursor.fetchall()

        objectList = []
        for row in result:
            jsonObject = Object()
            jsonObject.url = str(row[0]).replace("gifv", "mp4").replace("gif", "mp4")
            jsonObject.title = row[1]
            jsonObject.id = row[2]
            jsonObject.placeholder = str(row[0]).replace(".gifv", "h.jpg").replace(".gif", "h.jpg")
            jsonObject.reddit_id = row[3]
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
    ('/getposts_alternate', MainHandler)
], debug=True)
