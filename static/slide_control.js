

//////////////// Requires jQuery ////////////////


$('.left').click(function(){
	$.get('/remote/prior');
});

$('.right').click(function(){
	$.get('/remote/next');
});


document.onkeydown = function(evt) {
    evt = evt || window.event;
    // console.log(evt);

    // Left key
    if (evt.keyCode == 37) {
        $.get('/remote/prior');
    // Right key
    } else if (evt.keyCode == 39){
    	$.get('/remote/next');
    }
};