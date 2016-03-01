#! /bin/env python
# -*- coding: utf-8 -*-

"""API for purely client side viewing of `flask_slides`"""

from __future__ import print_function
import json
# from flask import Flask, json, render_template
import flask

from ... import flask_slides
# pylint: disable=W0312

# Perusal
#    - View
#        - list
#        - read


FLASK_SLIDES = flask_slides.FlaskSlides()

BP = flask.Blueprint('perusal', __name__, static_folder="static",
        static_url_path="/static/perusal", template_folder="templates")

@BP.route('/slides/', methods=['GET'])
def list_slides():
    """JSON view of list of slides available for viewing"""
    slides = sorted(FLASK_SLIDES.get_slides())

    data = []
    for idx, value in enumerate(slides):
        resource = {
                'type': 'slides',
                'id': str(idx),
                'links': {
                    'self': flask.url_for('perusal.get_slide', slide_id=idx)
                    },
                'attributes': {
                    'name': value
                    }
                }
        data.append(resource)

    return flask.jsonify({'data':data})

@BP.route('/slides/<slide_id>', methods=['GET'])
def get_slide(slide_id):
    """Render a particular slide by it's id"""
    slide_id = int(slide_id)

    slide_name = ""
    slide_body = ""
    slides_list = sorted(FLASK_SLIDES.get_slides())
    for idx, value in enumerate(slides_list):
        if idx == slide_id:
            slide_body = FLASK_SLIDES.render_slide(value)
            slide_name = value

    response = {
            "type": "slide",
            "id": str(slide_id),
            "attributes": {
                "title": slide_name,
                "body": slide_body
                }
            }
    return flask.jsonify(response)


@BP.route('/peruse')
def peruse_view():
    return flask.render_template('peruse.html')




