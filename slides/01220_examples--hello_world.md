Example Flask Applications
==========================

## Hello World

So small, I can put it right on this page!

<!--  -->

	#!python
	# Simple "Hello World"
	from flask import Flask
	app = Flask(__name__)

	@app.route('/')
	def root():
	    return "Whoo, first page!"

	if __name__ == '__main__':
	    app.run()