
//////////////// Slip.js ////////////////
//
// Slip.js is the Javascript that actually does the magic resizing of the
// current slide to best fit in the browser window. 
//
// In short, it applies a CSS "scale" to the div which contains the body of
// the slide. There's a listener for when the browser is resized, adjusting
// the scale on the slide div so that the div will always fit neatly within
// the window boundries.
//


var slip = (function(){
    var dom = {},
        config = {

            // The "normal" size of the presentation, aspect ratio will be preserved
            // when the presentation is scaled to fit different resolutions
            width: 960,
            height: 700,

            // Factor of the display size that should remain empty around the content
            margin: 0.1,

            minScale: 0.2,
            maxScale: 3.0
        };

    function initialize(){
        init_dom();

        // Adding our event listeners
        window.addEventListener( 'resize', onWindowResize, false );
        layout();
    }

    function init_dom(){
        // `dom.wrapper` isn't actually used, but keeping this here for
        // reference and in case anything goes wrong and I need to bring it
        // back.
        //
        // dom.wrapper = document.querySelector('#slip');
        dom.slides = document.querySelector('#slip #slides')
    }

    /**
    * Applies a CSS transform to the target element.
    */
    function transformElement( element, transform ) {
        element.style.WebkitTransform = transform;
        element.style.MozTransform = transform;
        element.style.msTransform = transform;
        element.style.OTransform = transform;
        element.style.transform = transform;
    }


    function layout(){
        // Much of this is taken from reveal.js (bless hakimel's soul for
        // having worked on this before me!)

        // Available space to scale within
        //
        // Originally used the dom.wrapper element, but I could only get it
        // working properly using `document.body`
        var availableWidth = document.body.offsetWidth,
            availableHeight = document.body .offsetHeight;

        // Reduce available space by margin
        availableWidth -= ( availableHeight * config.margin );
        availableHeight -= ( availableHeight * config.margin );

        // Dimensions of the content
        var slideWidth = config.width,
            slideHeight = config.height;

        // A chunk of code handling width based on percentage has been cut out
        // of here.

        // Determine scale of content to fit within available space
        scale = Math.min( availableWidth / slideWidth, availableHeight / slideHeight );
        
        // Respect max/min scale settings
        scale = Math.max( scale, config.minScale );
        scale = Math.min( scale, config.maxScale );

        dom.slides.style.width = slideWidth + 'px';
        dom.slides.style.height = slideHeight + 'px';

        // console.log();
        

        // Do the scale/transformation
        //
        // Originally this transformation was:
        //
        //     translate(-50%, -50%) scale('+ scale +') translate(50%, 50%)'
        //
        // Notice the additional translate on the end. I've removed it here
        // because it was messing up the display in my case.
        transformElement( dom.slides, 'translate(-50%, -50%) scale('+ scale +')' );
    };

    /**
    * Handler for the window level 'resize' event.
    */
    function onWindowResize( event ) {
        layout();
    }


    //////////// API ////////////

    return {
        initialize: initialize,
        // Layout not strictly needed as an external API, but added anyway.
        layout: layout
    }

})(); 

// Start up the auto-resizing
slip.initialize();
