Flask Conventions
=================

- Single file (optional, but recommended)

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
