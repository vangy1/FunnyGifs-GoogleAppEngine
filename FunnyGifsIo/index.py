import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        htmlToExecute = """<html>
<head>
<title>Funny Gifs</title>
<meta name="description" content="The funniest gifs on the internet">
<link type="text/css" rel="stylesheet" href="css/style_v1.2.css" media="screen,projection">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/css/materialize.min.css">
<meta property="og:site_name"   content="Funny Gifs">
<meta property="og:url" content="http://funnygifs.io">
<meta property="og:title" content="Funny Gifs - The funniest gifs on the internet">
<meta property="og:description" content="Laugh with the funniest gifs on the internet">
<meta property="og:type" content="website">
<meta property="og:image" content="images/logo512.png">
<meta property="og:image:width" content="512">
<meta property="og:image:height" content="512">
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<link rel="manifest" href="manifest.json">
		<link rel="icon" type="image/png" href="images/logo-48.png">
</head>
<body>
	<header class="nav-down">
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
        if (window.location.href.indexOf("gif.php") != -1) {
            checkIfUserHasExtension();
        }
        ga('set', 'dimension1', 'has extension');
        ga('send', 'pageview');
    };
    img.onerror = function () {
        hasExtension = false;
        if (window.location.href.indexOf("gif.php") != -1) {
            checkIfUserHasExtension();
        }
        ga('set', 'dimension1', 'no extension');
        ga('send', 'pageview');
    };


</script>
	<div id="container">
   	<div id="video-list"></div>
		<div id="loading"/>Loading...</div>
	</div>
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
</script>
<script src="js/script_v1.3.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.15.2/moment.min.js"></script>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
getVideos(100000);
</script>
	  <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/js/materialize.min.js"></script>
</body>
</html>"""
        self.response.write(htmlToExecute)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index', MainHandler)
], debug=True)
