import MySQLdb
import os
import webapp2

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

        sql = "SELECT id FROM archive WHERE url like '%.gifv'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            self.response("Error 51")
        self.response.write("""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">""")
        for row in result:
            self.response.write("<url><loc>http://funnygifs.io/gif.php?id=")
            self.response.write(row[0])
            self.response.write("</loc></url>")
        self.response.write("</urlset>")

app = webapp2.WSGIApplication([
    ('/sitemap', MainHandler)
], debug=True)
