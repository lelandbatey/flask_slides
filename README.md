Flask_Slides
============


Flask_Slides is a super small, super simple tool for presenting a slide-show using a web browser. The key to Flask_Slides is it's remote-view architecture. Instead of a single page that must be navigated via keyboard keys, it instead works by having one page that acts as the "view", and another page that does the controlling (next/previous slide).

Slide Display
-------------

Generally, web pages and traditional slides are displayed in fundamentally different ways: the contents of a web page will modify itself to fit the size and shape of a web page, while a slide will always display in exactly the same way (potentially with letterboxing if there's extra space on screen). To get a web page to display in the highly consistent style of a slide, I take advantage of the CSS3 `transform: scale` property to maintain a consistent aspect ratio of the contents of the page. The source for this can be found in the `static/slip.js` file.


API Layout
---------------

The API layout of Flask_Slides looks like this:

	/
	/list
	/view/*
	/interact
	/remote

### `/`

Displays a page with links to the "Present", "Remote", and "List" pages.

### `/list`

Prints a list of all the different slides that could be displayed, as well as static links to each slide. Great for perma-linking a slide.


### `/view/*`

By going to a `/view/{NAME_OF_SLIDE}` url, you see a rendered version of that slide, without any other information.


### `/interact`

`/interact` is the "view" page that displays the current slide.


### `/remote`

`/remote` is the "control" page, and is used to move forward and backward in the slides. Loading this page on your phone and using it like a remote control works great.




