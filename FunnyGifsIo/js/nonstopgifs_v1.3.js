var availableDocumentHeight = $(document).height();
var watchBuffer;
var nextVideo;
var vertical = document.currentScript.getAttribute("vertical");
var controls = document.currentScript.getAttribute("controls");

if (getCookie('max-id') == null || getCookie('min-id') == null) {
    getVideos(1000000, 1000000);
} else {
    getVideos(getCookie('min-id'), getCookie('max-id'));
}

function getVideos(min, max) {
    $.ajax({
        url: "http://funnygifs.media/getposts_alternate?vertical=" + vertical + "&minimum=" + min + "&maximum=" + max,
        success: function (data) {
            var video = data[0];
            nextVideo = data[1];
            if (controls == "disabled") {
                $("#gif-card-container").html('<div class="card"><div class="video-title"><h5 class="video-title-style">' + video.title + '</h5></div>' +
                    '<div class="video-outer-container">' +
                    '<video preload="auto" loop="loop" poster="' + video.placeholder + '" data-id="' + video.id + '">' +
                    '<source src="' + video.url + '" type="video/mp4"></video>' +
                    '</div>' +
                    '</div>');
            } else {
                $("#gif-card-container").html('<div class="card"><div class="video-title"><h5>' +
                    '<a class="video-title-style" target="_blank" href="http://funnygifs.io/gif?id=' + video.reddit_id + '&utm_source=extension&utm_medium=title">' + video.title + '</h5></a></div>' +
                    '<div class="video-outer-container">' +
                    '<a target="_blank" href="http://funnygifs.io/gif?id=' + video.reddit_id + '&utm_source=extension&utm_medium=on_gif"><video preload="auto" loop="loop" poster="' + video.placeholder + '" data-id="' + video.id + '">' +
                    '<source src="' + video.url + '" type="video/mp4"></video><a/>' +
                    '</div>' +
                    '<div class="share-controls-inner card-action">' +
                    '<a class="fb-share-link" href="https://www.facebook.com/sharer/sharer.php?u=http://funnygifs.io/gif?id=' + video.reddit_id + '" target="_blank">' +
                    'Share on Facebook' +
                    '</a>' +
                    '<a class="get-link" data-id="' + video.id + '">Get link</a>' +
                    '<div class="share-url" style="display:none">' +
                    '<input value="http://funnygifs.io/gif?id=' + video.reddit_id + '&utm_source=extension&utm_medium=get_link" type="text" readonly=""></div>' +
                    '</div>' +
                    '</div>');
                setLinkClickHandler();
            }
            insertNextButton();
            resizeHeights();
            setCookieValue(video.id);
            ga('send', 'event', 'gif', 'play', video.id);
            //prerenderNextPage(nextVideo.url);
            watchBuffer = setInterval(checkIfLoaded, 500);
        }
    });
}

function resizeHeights() {
    var availableGifCardHeight = availableDocumentHeight - $('#top').outerHeight() - $('#ad-container').outerHeight();
    if (availableGifCardHeight > 700) {
        availableGifCardHeight = 700;
    }
    $('#gif-card-container').css('height', availableGifCardHeight + 'px');
    var availableVideoHeight;
    if (controls == "disabled") {
        availableVideoHeight = availableGifCardHeight - $('.video-title').outerHeight();
    } else {
        availableVideoHeight = availableGifCardHeight - $('.video-title').outerHeight() - $('.share-controls-inner').outerHeight();
    }
    $('video').css('height', availableVideoHeight + 'px');
    $('video').css('max-height', availableVideoHeight + 'px');
    $('video')[0].play();
    $('#gif-card-container').css('visibility', 'visible');
    $('#ad-container').show();
}

function insertNextButton() {
    if (controls == "disabled") {
        $('.card').append(
            '<a href="/nonstopgifs.php?controls=' + controls + '&vertical=' + vertical + '&utm_source=next_button&utm_medium=next_button"><div id="next"><span class="helper"></span>' +
            '<div id="next-helper">' +
            '<i class="material-icons">skip_next</i>' +
            '<div id="text-next">Next</div>' +
            '</div>' +
            '</div></a>'
        );
    } else {
        $('.card').append(
            '<a href="/nonstopgifs.php?vertical=' + vertical + '&utm_source=next_button&utm_medium=next_button"><div id="next"><span class="helper"></span>' +
            '<div id="next-helper">' +
            '<i class="material-icons">skip_next</i>' +
            '<div id="text-next">Next</div>' +
            '</div>' +
            '</div></a>'
        );
    }
}

function nextLinkHandler() {
    $('#next').click(function () {
        location.reload();
    });
}

function setLinkClickHandler() {
    $(".get-link").off();
    $(".get-link").click(function () {
        var targetInputBox = $('.share-url');
        var displayValue = targetInputBox.css('display');
        if (displayValue == "none") {
            targetInputBox.css('display', 'inline-block');
        } else {
            targetInputBox.css('display', 'none');
        }
        ga('send', 'event', 'share actions', 'get link (extension)');
    });
}


function checkIfLoaded() {
    if ($('video')[0].readyState) {
        var videoDuration = $('video')[0].duration;
        var buffered = $('video')[0].buffered.end(0);
        if (buffered >= videoDuration) {
            var hint = document.createElement("link");
            hint.setAttribute("rel", "preload");
            hint.setAttribute("href", nextVideo.url);
            hint.setAttribute("as", "media");
            document.getElementsByTagName("head")[0].appendChild(hint);
            var hint = document.createElement("link");
            hint.setAttribute("rel", "preload");
            hint.setAttribute("href", nextVideo.placeholder);
            hint.setAttribute("as", "image");
            document.getElementsByTagName("head")[0].appendChild(hint);
            clearInterval(this.watchBuffer);
        }
    }
}


function setCookieValue(id) {
    if (getCookie('max-id') == null) {
        setCookie('max-id', id, 20 * 365);
        setCookie('min-id', id, 20 * 365);
    } else {
        if (id > getCookie('max-id')) {
            setCookie('max-id', id, 20 * 365);
        } else {
            setCookie('min-id', id, 20 * 365);
        }
    }
}


function setCookie(key, value) {
    var expires = new Date();
    expires.setTime(expires.getTime() + (1 * 24 * 60 * 60 * 1000));
    document.cookie = key + '=' + value + ';expires=' + expires.toUTCString();
}

function getCookie(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
}
