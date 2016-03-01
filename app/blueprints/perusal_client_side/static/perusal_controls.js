"use strict";

function PeruseControl(){
	this.load_slides().then(() =>{
		try {
			if (!!window.location.hash){
				let hsh_num = parseInt(window.location.hash.substring(1), 10);
				this.current_slide = hsh_num;
			} else {
				this.current_slide = 0;
			}
		} catch (e){
			this.current_slide = 0;
			location.replace('#'+this.current_slide);
		}
	});
}

/**
 * @brief Load the metadata about the available slides into this object.
 */
PeruseControl.prototype.load_slides = function(){return new Promise((resolve, reject) => {
	$.get('/slides/', data => {
		this.slide_data = data['data'];
		resolve();
	});
});};


/**
 * @brief Re-draws the visible contents of the slide with the body of the slide
 * with `id` equal to `this.current_slide`.
 */
PeruseControl.prototype.draw_current_slide = function(){return new Promise((resolve, reject) => {
	if (!this.slide_data) {
		resolve();
	}
	var idx = this.current_slide;
	$.get('/slides/'+idx, data => {
		// Update the '#/#' indicator in the bottom right showing the current
		// slide and how many remain.
		document.querySelector('#slide_index').innerHTML = idx+" / "+(this.slide_data.length-1);

		// Update the body of the page
		var slide_body = data['attributes']['body'];
		var slide_elem = document.querySelector('#slides');
		slide_elem.innerHTML = slide_body;

		// Update the page location
		location.replace('#'+this.current_slide);
		resolve();
	});
});};

PeruseControl.prototype.next_slide = function(){return new Promise((resolve, reject) => {
	let slide_count = this.slide_data.length - 1;
	if (this.current_slide < slide_count) {
		this.current_slide = this.current_slide + 1;
		this.draw_current_slide()
			.then(resolve);
	} else {
		resolve();
	};
});};

PeruseControl.prototype.previous_slide = function(){return new Promise((resolve, reject) => {
	if ((this.current_slide - 1) >= 0) {
		this.current_slide = this.current_slide - 1;
		this.draw_current_slide()
			.then(resolve);
	} else {
		resolve();
	};
});};




// Instantiate object, draw the slides
window.__PERUSAL = new PeruseControl();
__PERUSAL.load_slides()
	.then(_ => window.__PERUSAL.draw_current_slide());

// Cause the arrow keys to move between slides.
document.onkeydown = function(evt) {
    evt = evt || window.event;
	//console.log(evt);

    // Left key
    if (evt.keyCode == 37) {
		window.__PERUSAL.previous_slide();

    // Right key
    } else if (evt.keyCode == 39){
		window.__PERUSAL.next_slide();
		//__PERUSAL.next_slide();
    }
};


document.addEventListener('touchstart', handleTouchStart, false);        
document.addEventListener('touchmove', handleTouchMove, false);

// Code from stackoverflow to handle swipe event on mobile phones
//     http://stackoverflow.com/a/23230280
var xDown = null;
var yDown = null;

function handleTouchStart(evt) {
    xDown = evt.touches[0].clientX;
    yDown = evt.touches[0].clientY;
};

function handleTouchMove(evt) {
    if ( ! xDown || ! yDown ) {
        return;
    }

    var xUp = evt.touches[0].clientX;
    var yUp = evt.touches[0].clientY;

    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;

    if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/*most significant*/
        if ( xDiff > 0 ) {
            /* left swipe */ 
			window.__PERUSAL.next_slide();
        } else {
            /* right swipe */
			window.__PERUSAL.previous_slide();
        }
    } else {
        if ( yDiff > 0 ) {
            /* up swipe */ 
        } else { 
            /* down swipe */
        }
    }
    /* reset values */
    xDown = null;
    yDown = null;
};




