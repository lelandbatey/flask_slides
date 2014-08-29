<style type="text/css">
.highlighttable {
	line-height: 1.1em;
}
</style>

`Request` and `Response` Objects
================================

- Interacting with requests is easy
- Building complicated responses is simple

<!--  -->

	#!python
	import flask
	from flask import Flask, request, response
	from pdf_converter import make_pdf # Fake library

	@app.route('/api/md2pdf/', methods=['POST'])
	def buildPdf():
	    body = request.form['body_text']

	    response = flask.make_response(makePdf(body))
	    response.headers['Content-type'] = "application/pdf"

	    return response