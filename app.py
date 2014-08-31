#! /bin/env python
from __future__ import print_function
from flask import Flask, request, json, render_template, Response
from pprint import pprint
import flask_slides
import urllib2

slide = flask_slides.flask_slides()
app = Flask(__name__)

slide_list = []

def jsonDump(inDat):
	return json.dumps(inDat, sort_keys=True, indent=4, separators=(',', ': '))
def jp(inDat):
	print(jsonDump(inDat))

@app.route('/')
def root():
	return render_template('front.html', name="Frontpage")


@app.route('/list/')
def list():
	slides = sorted(slide.get_slides().keys())

	return render_template('list.html', slideList = slides)
	# return Response(jsonDump(slides), mimetype='text/plain' )


@app.route('/view/<slide_name>')
def view(slide_name):
	slide_output = slide.render_slide(slide_name)
	return render_template('slide_page.html', slide=slide_output, name=slide_name)


@app.route('/present')
def present():
	return render_template('slide_page.html',slide=slide.render_index(slide.index), name ="Presenting", live=True)


@app.route('/present/index')
def present_index():
	"""Returns index of current slide.

	Client uses this to see if the slide has changed.
	"""
	return str(slide.index)

@app.route('/present/total_slides')
def total_slides():
	"""Returns total number of slides in deck."""
	return str(len(slide.get_slide_list()))


# Sends the contents of the slide, but doesn't render the entire page. Used by
# the client to update the body of the slide page.
@app.route('/present/current_slide')
def present_current_slide():
	return slide.render_index(slide.index)


@app.route('/remote')
def remote():
	return render_template("remote.html")


@app.route('/remote/next')
def next():
	slide.index += 1
	print(slide.index)
	return ""


@app.route('/remote/prior')
def prior():
	slide.index -= 1
	# print(slide.index)
	return ""

@app.route('/error')
def error():
	return var_that_doesnt_exist


@app.route('/prox/<path:requestPath>')
def prox(requestPath):
	data = urllib2.urlopen(requestPath).read()
	return data


# list()

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

