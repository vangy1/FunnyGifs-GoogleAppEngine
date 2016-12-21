import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""<html>
<head>
<title>Funny Gifs</title>
<meta name="description" content="The funniest gifs on the internet">
<link type="text/css" rel="stylesheet" href="css/style_v1.2.css" media="screen,projection">
<link type="text/css" rel="stylesheet" href="css/nonstopgifs.css" media="screen,projection">
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
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>
<body>
		<script>
			(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
			(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
			m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
			})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

			ga('create', 'UA-65897021-4', 'auto');
			ga('send', 'pageview');;

		</script>
		<div id="top"></div>
   	<div id="gif-card-container"></div>
		<div id="ad-container" style="display:block;text-align:center">
			<ins class="adsbygoogle"
     style="display:inline-block;width:468px;height:60px"
     data-ad-client="ca-pub-8788434869539504"
     data-ad-slot="1056780635"></ins>
		</div>
<script src="js/nonstopgifs_v1.3.js"></script>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
	var random = Math.random();
	if (random < 0.5){
		(adsbygoogle = window.adsbygoogle || []).push({});
	}
</script>
</body>
</html>""")


app = webapp2.WSGIApplication([
    ('/nonstopgifs.php', MainHandler)
], debug=True)
