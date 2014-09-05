<style type="text/css">
.highlighttable {
	line-height: 1em;
}
</style>
Example Flask Applications
==========================

## Simple Proxy


<!--  -->


	#!python
	from flask import Flask
	import urllib2
	app = Flask(__name__)

	@app.route('/<path:requestPath>')
	def proxy(requestPath):
	    data = urllib2.urlopen(requestPath).read()
	    return data

	@app.route('/')
	def root():
	    return "Enter a url above to proxy it through."

	if __name__ == '__main__':
	    app.run(host= '0.0.0.0')