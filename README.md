Flask_Slides
============


Flask_Slides is a super small, super simple tool for presenting a slide-show using a web browser. The key to Flask_Slides is it's remote-view architecture. Instead of a single page that must be navigated via keyboard keys, it instead works by having one page that acts as the "view", and another page that does the controlling (next/previous slide).


Layout
------

The internal layout of Flask_Slides looks like this:

	/
	/list
	/view/*
	/interact
	/remote

### `/interact` 

`/interact` is the "view" page that displays the current slide.


### `/remote`

`/remote` is the "control" page. You'd do something like load this page on the current 


### `/list`

Prints a list of all the different slides that could be displayed.


### `/view/*`

By going to a `/view/{slideName}` url, you see a rendered version of that slide, without any other information.










