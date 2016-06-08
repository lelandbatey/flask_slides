#! /bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import flask
import sys

from app import frontend
from app import flask_slides
from app.blueprints.perusal_client_side import perusal

APP = frontend.APP
APP.register_blueprint(perusal.BP)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        slides_path = sys.argv[1]
        APP.config['SLIDES'] = flask_slides.FlaskSlides(slides_path)
    APP.run(debug=True, host="0.0.0.0")
