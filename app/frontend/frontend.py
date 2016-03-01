#! /bin/env python
# -*- coding: utf-8 -*-

"""Coordinator and HTTP handler for `flask_slides`."""

from __future__ import print_function
from flask import Flask, json, render_template
from .. import flask_slides
import urllib2
# pylint: disable=W0312

FLASK_SLIDES = flask_slides.FlaskSlides(slides_dir='./slides')
APP = Flask(__name__)


# These are just some pet debug functions I love to have around. You'll
# probably find them all over the place. It's lazy and I don't care.
def jdump(obj):
    """Return json string representation of object"""
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
def jprint(obj):
    """Print a json representation of a given object"""
    print(jdump(obj))


@APP.route('/')
def root():
    """Render the front page"""
    return render_template('front.html', name="Frontpage")


@APP.route('/list/')
def list_slides():
    """Render a list of slides"""
    slides = sorted(FLASK_SLIDES.get_slides().keys())
    return render_template('list.html', slideList=slides)


@APP.route('/view/<slide_name>')
def view(slide_name):
    """Render a particular slide by name"""
    slide_output = FLASK_SLIDES.render_slide(slide_name)
    return render_template('slide_page.html', slide=slide_output, name=slide_name)


@APP.route('/present/')
def present():
    """Renders the slide page, including the current FLASK_SLIDES. This means the
    javascript doesn't have to load the slide, so there's no lag/delay.
    """
    return render_template('slide_page.html',
                           slide=FLASK_SLIDES.render_index(FLASK_SLIDES.index),
                           name="Presenting", live=True)


@APP.route('/present/index')
def present_index():
    """Returns index of current FLASK_SLIDES.

    Client uses this to see if the slide has changed.
    """
    return str(FLASK_SLIDES.index)

@APP.route('/present/total_slides')
def total_slides():
    """Returns total number of slides in deck."""
    return str(len(FLASK_SLIDES.get_slide_list()))


# Sends the contents of the slide, but doesn't render the entire page. Used by
# the client to update the body of the slide page.
@APP.route('/present/current_slide')
def present_current_slide():
    """Returns contents of slide without rendering an entire page."""
    return FLASK_SLIDES.render_index(FLASK_SLIDES.index)


@APP.route('/remote')
def remote():
    """Renders the 'remote control' interface for changing slides"""
    return render_template("remote.html")


# Because I am an EXTREMELY lazy person, these are simple GET requests that
# modify state. It's not a very flexible way of modifying the state, since it
# only allows for incrementing from one slide to another. A more flexible way
# would be to have this be a post request that takes a variable that's
# supposed to be the slide to switch to.
@APP.route('/remote/next')
def next_slide():
    """Increment the current slide"""
    FLASK_SLIDES.index += 1
    return ""
@APP.route('/remote/prior')
def prior():
    """Decrement the current slide"""
    FLASK_SLIDES.index -= 1
    return ""


# This is intentionally throws an error, since it's used in one of the slides.
@APP.route('/error')
def error():
    """Intentionally causes an error to demonstrate flasks debugging"""
    return var_that_doesnt_exist

# Trivial example of proxy which I included because I think I may use it in my
# presentation. Might not though. We'll see.
@APP.route('/prox/<path:request_path>')
def prox(request_path):
    """Acts as a trivial example of a proxy, for use in presentation."""
    data = urllib2.urlopen(request_path).read()
    return data



if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=5000)

