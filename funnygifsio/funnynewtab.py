import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        htmlToExecute = """<html>
  <head>
    <title>Funny New Tab - Get the Chrome Extension</title>
    <meta name="description" content="Laugh with the funniest gifs every time you open a new tab. Get the Chrome extension!">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.7/css/materialize.min.css">
        <link rel="icon" type="image/png" href="images/logo-48.png">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        <link rel="chrome-webstore-item" href="https://chrome.google.com/webstore/detail/pgomiemfankmkbmlkelacahjoocegcgm">
    <meta property="og:site_name"   content="Funny Gifs">
    <meta property="og:url" content="http://funnygifs.io">
        <meta property="og:title" content="Funny Gifs">
        <meta property="og:description" content="Laugh with the funniest gifs every time you open a new tab. Get the Chrome extension!">
        <meta property="og:type" content="website">
        <meta property="og:image" content="http://funnygifs.io/images/rectangle-promo.png">
    <style>
      #promo-section{
          margin-top:30px;
      }
      #promo-header{
          margin:0px 0px 40px 0px;
          font-family:'Open Sans', sans-serif;
          padding:20px;
      }
      #promo-logo{
          text-align:center;
      }
      #promo-logo img{
          width:130px;
      }
      #promo-message{
          font-size:19px;
          text-align:center;
          color:#666;
          margin:30px;
      }
      #install-button{
          text-align:center;
      }
      #success-message{
          color:green;
          font-size:20px;
      }
      #promo-image{
          text-align:center;
      }
      .button {
        font-family: Roboto;
        display: inline-block;
        margin: 0.3em;
        padding: 10px 20px;
        overflow: hidden;
        position: relative;
        text-decoration: none;
        border-radius: 3px;
        -webkit-transition: 0.3s;
        -moz-transition: 0.3s;
        -ms-transition: 0.3s;
        -o-transition: 0.3s;
        transition: 0.3s;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        border: none; 
        font-size: 17px;
        text-align: center;
        cursor:pointer;
      }

      .button:hover {
        box-shadow: 1px 6px 15px rgba(0,0,0,0.5);
      }

      .blue {
        background-color: #03A9F4;
        color: white;
      }

      .ripple {
        position: absolute;
        background: rgba(0,0,0,.25);
        border-radius: 100%;
        transform: scale(0.2);
        opacity:0;
        pointer-events: none;
        -webkit-animation: ripple .75s ease-out;
        -moz-animation: ripple .75s ease-out;
        animation: ripple .75s ease-out;
      }

      @-webkit-keyframes ripple {
        from {
          opacity:1;
        }
        to {
          transform: scale(2);
          opacity: 0;
        }
      }

      @-moz-keyframes ripple {
        from {
          opacity:1;
        }
        to {
          transform: scale(2);
          opacity: 0;
        }
      }

      @keyframes ripple {
        from {
          opacity:1;
        }
        to {
          transform: scale(2);
          opacity: 0;
        }
      }

      #footer{
          bottom:0px;
          right:3px;
          position:fixed;
          z-index:200;
          font-size:11px;
          width:100%;
          text-align: right;
      }

      #footer div{
        margin-right:5px;
        display: inline-block;
      }
      #footer img{
        opacity: 0.5;
          height: 22px;
      }

      #star-rating{
       font-size:23px;
      }
      #star-rating span{
          margin-left:-4px;
      }
      #star-rating .full{
          color:gold;
      }
      #star-rating .empty{
          color:#eaeaea;
      }
    </style>
  </head>
  <body>
    <script>
        
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
    
      ga('create', 'UA-65897021-4', 'auto');
      ga('send', 'pageview');
    
    </script>
  
  
    <div id="container">
        <div id="">
            <div style="text-align:center;background-color:#FFDA00">
                <img style="height:400px;" src="images/marquee.png" />
            </div>
        </div>
        <div id="promo-section">
            <div id="promo-header">
                <div id="install-button">
                    <a class="button blue install">
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
    </div>
  </body>
  <script>
    
$(".install").click(function(){
    if (isMobile == false){
        chrome.webstore.install("https://chrome.google.com/webstore/detail/pgomiemfankmkbmlkelacahjoocegcgm",successCallback)
    } else {
        window.location = 'https://chrome.google.com/webstore/detail/funny-new-tab/pgomiemfankmkbmlkelacahjoocegcgm';
    }
});

function successCallback(){
    $("#install-button").html("<div id='success-message'>Great! Now try opening a new tab</div>");
    if (location.href.indexOf('gif.php') != -1){
        var dimensionValue = 'shareable page';
    } else {
        var dimensionValue = 'homepage';
    }
    ga('set', 'dimension1', dimensionValue);
    ga('send', 'pageview', {'page': '/extension-promo-page-install'})
}



$('.button').mousedown(function (e) {
    var target = e.target;
    var rect = target.getBoundingClientRect();
    var ripple = target.querySelector('.ripple');
    $(ripple).remove();
    ripple = document.createElement('span');
    ripple.className = 'ripple';
    ripple.style.height = ripple.style.width = Math.max(rect.width, rect.height) + 'px';
    target.appendChild(ripple);
    var top = e.pageY - rect.top - ripple.offsetHeight / 2 -  document.body.scrollTop;
    var left = e.pageX - rect.left - ripple.offsetWidth / 2 - document.body.scrollLeft;
    ripple.style.top = top + 'px';
    ripple.style.left = left + 'px';
    return false;
});


  </script>
</html>"""
        self.response.write(htmlToExecute)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/funnynewtab', MainHandler)
], debug=True)
