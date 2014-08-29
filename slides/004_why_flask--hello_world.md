Why Flask?
==========

- Flask is small

<p></p>

	#!python
	from flask import Flask
	# Simple "Hello World"

	app = Flask(__name__)

	@app.route('/')
	def root():
	    return "Whoo, first page!"

	if __name__ == '__main__':
	    app.run()

