var isMobile = false; //initiate as false
// device detection
if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) isMobile = true;
    
    setLinkClickHandler();
		//adjust height of primary video
		$(".primary").css("max-height",(window.innerHeight * 0.45) + 'px');
	
		var videos;
		var videoPos;
		var loaded;
		var videosRemaining;
		var activeVideoRequest = true;;
		function getVideos(before){
			$.ajax({
			url: "http://funnygifs.io/getposts_web_client?size=5&before="+before,
			success: function(data){
	        	data.forEach(function(video){
	        		$("#video-list").append('<div class="video-item card"><div class="video-title"><h5>'+
							'<a class="video-title-style" href="http://funnygifs.io/gif?id='+video.id+'">'+video.title+'</h5></a></div>'+
							'<div class="timestamp row">'+moment(video.timestamp * 1000).fromNow()+'</div>'+
			  			'<div class="video-outer-container">'+
		  					'<video preload="auto" loop="loop" poster="'+video.placeholder+'" data-id="'+video.id+'">'+
		  					'<source src="'+video.url+'" type="video/mp4"></video>'+
			  			'</div>'+
							'<div class="mobile-share card-action"><a class="white black-text waves-effect waves-light btn modal-trigger" data-id="'+video.id+'" href="#modal1">Share</a></div>'+																			
							'<div class="share-controls-inner row card-action">'+
									'<a class="fb-share-link" href="https://www.facebook.com/sharer/sharer.php?u=http://funnygifs.io/gif?id='+video.id+'" target="_blank">'+
										'Share on Facebook'+
									'</a>'+
									'<a class="get-link" data-id="'+video.id+'">Get link</a>'+
								'<div class="share-url" style="display:none" id="input-'+video.id+'">'+
									'<input value="http://funnygifs.io/gif?id='+video.id+'" type="text" readonly=""></div>'+
							'</div>'+
			  		'</div>')
	        	});
					activeVideoRequest = false;
					// the list of our video elements
					videos = document.querySelectorAll('video');
					if (!isMobile){videos[0].play();}
					// an array to store the top and bottom of each of our elements
					videoPos = [];
					// a counter to check our elements position when videos are loaded
					loaded = 0;
					// add the scrollHandler
					window.addEventListener('scroll', scrollHandler, true);
					// don't forget to update the positions again if we do resize the page
					window.addEventListener('resize', checkPos);
					checkPos();
          setLinkClickHandler()
					$('.modal-trigger').leanModal();
					calculateGifPlays();
					$('#video-list').append('<div class="in-feed-ad"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8788434869539504" data-ad-slot="3978064231" data-ad-format="auto"></ins></div>');
					(adsbygoogle = window.adsbygoogle || []).push({});
			}
		});
		}



		// Here we get the position of every element and store it in an array
		function checkPos() {
		  // loop through all our videos
		  for (var i = 0; i < videos.length; i++) {
        
        //adjust for mobile
        if (isMobile){
          videos[i].controls = true;
					videos[i].setAttribute("muted","muted");
					videos[i].setAttribute("autoplay","autoplay");
					videos[i].setAttribute("webkit-playsinline","");
          //videos[i].style.width = "100%";
					//videos[i].style.maxHeight = '276px';
        } else {
					//videos[i].style.maxHeight = '476px';
				}
		    var element = videos[i];
		    // get its bounding rect
		    var rect = element.getBoundingClientRect();
		    // we may already have scrolled in the page 
		    // so add the current pageYOffset position too
		    var top = rect.top + window.pageYOffset;
		    var bottom = rect.bottom + window.pageYOffset;
		    // it's not the first call, don't create useless objects
		    if (videoPos[i]) {
		      videoPos[i].el = element;
		      videoPos[i].top = top;
		      videoPos[i].bottom = bottom;
		    } else {
		      // first time, add an event listener to our element
		      element.addEventListener('loadeddata', function() {
		          if (++loaded === videos.length - 1) {
		            // all our video have ben loaded, recheck the positions
		            // using rAF here just to make sure elements are rendered on the page
		            requestAnimationFrame(checkPos)
		          }
		        })
		        // push the object in our array
		      videoPos.push({
		        el: element,
		        top: top,
		        bottom: bottom
		      });
		    }
		  }
		};
		// an initial check


		var scrollHandler = function() {
		  // our current scroll position

		  // the top of our page
		  var min = window.pageYOffset;
		  // the bottom of our page
		  var max = min + window.innerHeight;

		  videoPos.forEach(function(vidObj) {
		    // the top of our video is visible
		    if (vidObj.top >= min && vidObj.top < max) {
		      // play the video
		      if (!isMobile){vidObj.el.play();}
		      videosRemaining = videos.length - videoPos.indexOf(vidObj) -1;
		      //console.log(videosRemaining + " videos left and "+videos.length+ " videos in total");
		      if (videosRemaining == 2 && activeVideoRequest == false){
            var before = videos[videos.length - 1].getAttribute('data-id');
		      	getVideos(before);
		      	activeVideoRequest = true;
		      }
		    }

		    // the bottom of the video is above the top of our page
		    // or the top of the video is below the bottom of our page
		    // ( === not visible anyhow )  
		    if (vidObj.bottom <= min || vidObj.top >= max) {
		      // stop the video
		      if (!isMobile){vidObj.el.pause();}
		    }

		  });
		};
	
	function setLinkClickHandler(){
    $(".get-link").off();
		$(".get-link").click(function(){
      var targetInputBox = $(this).parent().find('.share-url');
			var displayValue = targetInputBox.css('display');
			if (displayValue == "none"){
				targetInputBox.css('display','inline-block');
			} else {
				targetInputBox.css('display','none');
			}
			ga('send', 'event', 'share actions', 'get link (desktop)');
		});
		
		$('.modal-trigger').click(function(){
			var title = $(this).parent().parent().find('.video-title').text();
			var url="http://funnygifs.io/gif?id="+$(this).attr('data-id');
			addthis.update('share', 'url', url);
			addthis.update('share', 'title', title);
			ga('send', 'event', 'share actions', 'open mobile share modal');
    	}
  	);
	}


var didScroll;
var lastScrollTop;
var delta;
var navbarHeight;

$(document).ready(function(){
	// Hide Header on on scroll down
	lastScrollTop = 0;
	delta = 5;
	navbarHeight = $('header').outerHeight();

	$(window).scroll(function(event){
			didScroll = true;
	});

	setInterval(function() {
			if (didScroll) {
					hasScrolled();
					didScroll = false;
			}
	}, 250);
});

function hasScrolled() {
    var st = $(this).scrollTop();    
    // Make sure they scroll more than delta
    if(Math.abs(lastScrollTop - st) <= delta)
        return;
    
    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (st > lastScrollTop && st > navbarHeight){
        // Scroll Down
        $('header').removeClass('nav-down').addClass('nav-up');
    } else {
        // Scroll Up
        if(st + window.innerHeight < $(document).height()) {
            $('header').removeClass('nav-up').addClass('nav-down');
        }
    }
    
    lastScrollTop = st;
}

function calculateGifPlays(){
	$('video').on('play', function(event) {
		var currentId = $(this).attr('data-id');
		if (!playedGifs.includes(currentId)){
			playedGifs.push(currentId);
			ga('send', 'event', 'gif','play',currentId );
		}
	});
}

