Routes
======

What's a Route?
---------------

- Binds a function to a URL
- Uses the `route()` decorator for easy binding 

<!--  -->

	#!python
	@app.route('/')
	def index():
	    return 'Index Page'

	@app.route('/hello')
	def hello():
	    return 'Hello World'