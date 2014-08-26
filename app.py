from __future__ import print_function
from flask import Flask, request, json, render_template, Response
import flask_slides

slide = flask_slides.flask_slides()
app = Flask(__name__)


def jsonDump(inDat):
	return json.dumps(inDat, sort_keys=True, indent=4, separators=(',', ': '))
def jp(inDat):
	print(jsonDump(inDat))

@app.route('/')
def root():
	return render_template('frontpage.html')


@app.route('/list/')
def list():
	slides = slide.get_slides()
	return Response(jsonDump(slides), mimetype='text/plain' )


@app.route('/view/<slide_name>')
def view(slide_name):
	slide_output = slide.render_slide(slide_name)
	return render_template('frontpage.html', slide=slide_output, name=slide_name)




# list()

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

