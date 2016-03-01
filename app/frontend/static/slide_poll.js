
// Requires jQuery to work

//////////////// Poll Script ////////////////
//
// Every 250 milliseconds, we check if the current-server-slide is the same as
// the client-slide. If the servers differs from the clients, we download the
// new page and re-build the slide display.
//


function update_slide(slide_index){
	$.ajax({
		url: '/present/current_slide',
		cache: false,
		success: function(slide_contents){
			// Update the slide counter in the bottom right corner.
			$.get('/present/total_slides', function(total_slides){
				total_slides = (+total_slides)-1; // To prevent off-by-one in display
				document.querySelector('#slide_index').innerHTML = slide_index+" / "+total_slides;
				
				// Then update the contents of the slide
				var slides = document.querySelector('#slides');
				slides.innerHTML = slide_contents;
			});
		}
	});

}


// Updates the contents of the slide div by polling the server.
function poll(){
	setTimeout(function(){
		$.ajax({
			url: '/present/index',
			cache: false,
			success: function(data){
				// If the slide has changed, get the contents of the new slide
				// and update the page.
				if (data != current_slide_index){
					// console.log(data);
					// console.log(current_slide_index);
					current_slide_index = data;
					update_slide(data);
				};
			poll(current_slide_index);
			}
		});
	},250);
};


var current_slide_index = "what";

poll();


