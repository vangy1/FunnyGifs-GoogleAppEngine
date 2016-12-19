# Import libraries
import re
import MySQLdb
import os
import webapp2
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

        self.response.write("""<html><head><title>""")
        self.response.write(title)
        self.response.write(""" - Funny Gifs</title>
<meta name="description" content="The funniest gifs on the internet">
<meta property="og:site_name"   content="Funny Gifs">
<meta property="og:url" content="http://funnygifs.io/gif?id=""")
        self.response.write(id)
        self.response.write("""\"><meta property="og:title" content=\"""")
        self.response.write(title)
        self.response.write("""\">
<meta property="og:description" content="The funniest gifs on the internet">
<meta property="og:type" content="website">
<meta property="og:image" content=\"""")
        self.response.write(image)
        self.response.write("""\">
<meta property="og:image:width" content="480">
<meta property="og:image:height" content="270">
<link type="text/css" rel="stylesheet" href="css/style_v1.2.css" media="screen,projection">
<link type="text/css" rel="stylesheet" href="css/extension-promo.css" media="screen,projection">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/css/materialize.min.css">
<link rel="chrome-webstore-item" href="https://chrome.google.com/webstore/detail/pgomiemfankmkbmlkelacahjoocegcgm">
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<link rel="manifest" href="manifest.json">
	<link rel="icon" type="image/png" href="images/logo-48.png">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="js/extension-promo.js"></script>
</head>
<body><header class="nav-down">
    <div id="center-header">
        <a href="/">
            <div id="logo"><img src="images/logo48.png"></div>
            <div id="site-name">Funny Gifs</div>
        </a>
    </div>
</header>
<script>
    (function (i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function () {
                    (i[r].q = i[r].q || []).push(arguments)
                }, i[r].l = 1 * new Date();
        a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m)
    })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

    ga('create', 'UA-65897021-4', 'auto');

    var img;
    var hasExtension;
    img = new Image();
    img.src = "chrome-extension://pgomiemfankmkbmlkelacahjoocegcgm/images/icon-16x16.png";
    img.onload = function () {
        hasExtension = true;
        if (window.location.href.indexOf("gif") != -1) {
            checkIfUserHasExtension();
        }
        ga('set', 'dimension1', 'has extension');
        ga('send', 'pageview');
    };
    img.onerror = function () {
        hasExtension = false;
        if (window.location.href.indexOf("gif") != -1) {
            checkIfUserHasExtension();
        }
        ga('set', 'dimension1', 'no extension');
        ga('send', 'pageview');
    };


</script>
<div id="container">
		<div class="video-item video-item-primary row card">
			<div class="video-title"><h5>""")
        self.response.write(title)
        self.response.write("""</h5></div>
			<div class="video-outer-container">
				<video class="primary" webkit-playsinline muted="muted" preload="auto" loop="loop" poster=\"""")
        self.response.write(image)
        self.response.write("""\" data-id=\"""")
        self.response.write(id)
        self.response.write("""\"><source src=\"""")
        self.response.write(url)
        self.response.write("""\" type="video/mp4">
				</video>
			</div>
			<div class="mobile-share card-action"><a class="white black-text waves-effect waves-light btn modal-trigger" data-id=\"""")
        self.response.write(id)
        self.response.write("""\" href="#modal1">Share</a></div>
			<div class="share-controls-inner card-action">
					<a class="fb-share-link" href="https://www.facebook.com/sharer/sharer.php?u=http://funnygifs.io/gif?id=""")
        self.response.write(id)
        self.response.write("""\" target="_blank">
					Share on Facebook
					</a>
					<a class="get-link" data-id=\"""")
        self.response.write(id)
        self.response.write("""\">Get link</a>
				<div class="share-url" style="display:none" id="input-""")
        self.response.write(id)
        self.response.write("""\"><input value="http://funnygifs.io/gif?id=""")
        self.response.write(id)
        self.response.write("""\" type="text" readonly=""></div>
			</div>
			<div id="extension-promo">
				<div>
					 <span style="font-weight:bold">TIP: </span>Enjoy the funniest gifs right on Chrome's new tab page
				</div>
				<div class="btn" id="install-button">
					Get <span style="font-weight:bold">Funny New Tab</span> for Chrome
					<div id="star-rating">
							<span class="full">&#9733;</span>
							<span class="full">&#9733;</span>
							<span class="full">&#9733;</span>
							<span class="full">&#9733;</span>
							<span class="empty">&#9733;</span>
					</div>
					</a>
				</div>
			</div>
		</div>
		<div class="gif-page-ad">
				<ins class="adsbygoogle"
			 style="display:inline-block;width:468px;height:60px"
			 data-ad-client="ca-pub-8788434869539504"
			 data-ad-slot="1530798630"></ins>
		</div>
		<div id="video-list"></div>
			<div class="row" style="text-align:center;">
				<a class="white waves-effect waves-light btn" id="load-more-gifs">Continue</a>
			</div>
		<div id="loading" style="display:none;"/>Loading...</div>
		 <div id="modal1" class="modal bottom-sheet">
    <div class="modal-content">
      <h4>Share</h4>
      <p>
				<script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-5812a010404ff18f"></script>
				<div class="addthis_inline_share_toolbox">
				</div>
			</p>
    </div>
    <div class="modal-footer">
      <a href="#!" class=" modal-action modal-close waves-effect waves-green btn-flat">Close</a>
    </div>
  </div>

<script>
	var playedGifs = [];
	$(document).ready(function(){

		if (isMobile){
			var videos = document.querySelectorAll('video');
    	videos[0].controls = true;
    }

    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();
		setLinkClickHandler();

		$('#load-more-gifs').click(function(){
			$('#loading').show();
			getVideos(1000000);
			ga('send', 'event', 'load more gifs', 'load more gifs');
			$(this).parent().remove();
		});
		calculateGifPlays();
		$('.primary')[0].play();
  });
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.15.2/moment.min.js"></script>
<script src="js/script_v1.3.js"></script>
<script>
	if (!isMobile){
			(adsbygoogle = window.adsbygoogle || []).push({});
	}
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/js/materialize.min.js"></script>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<link itemprop="thumbnailUrl" href=\"""")
        self.response.write(image)
        self.response.write("""\">
<span itemprop="thumbnail" itemscope itemtype="http://schema.org/ImageObject">
<link itemprop="url" href=\"""")
        self.response.write(image)
        self.response.write("""\">
</span>
</body>
</html>""")


app = webapp2.WSGIApplication([
    ('/gif', MainHandler),
    ('/gif.php', MainHandler)
], debug=True)
