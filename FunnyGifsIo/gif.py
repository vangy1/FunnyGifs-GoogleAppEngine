# Import libraries
import re
import jinja2
import MySQLdb
import os
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# -----------------

class MainHandler(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id', 0)

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

        if re.search('t3_.{6}',id):
            sql = "SELECT url,title,id,reddit_id,permalink FROM archive where reddit_id = '%s'" % (str(id))
        else:
            sql = "SELECT url,title,id,reddit_id,permalink FROM archive where id = '%d'" % (int(id));

        cursor.execute(sql)
        result = cursor.fetchall()

        title = ""
        id = ""
        reddit_id = ""
        permalink = ""
        image = ""

        for row in result:
            url = str(row[0]).replace("gifv", "mp4").replace("gif", "mp4")
            title = row[1]
            id = row[2]
            reddit_id = row[3]
            permalink = "http://reddit.com" + row[4]
            image = str(row[0]).replace(".gifv", "h.jpg").replace(".gif", "h.jpg")

        template_values = {
            'title': title,
            'image': image,
            'id': id,
            'url': url
        }

        template = JINJA_ENVIRONMENT.get_template('html/gif.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/gif', MainHandler),
    ('/gif.php', MainHandler)
], debug=True)
