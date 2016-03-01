#! /bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import flask

from app import frontend
from app.blueprints.perusal_client_side import perusal

APP = frontend.APP
APP.register_blueprint(perusal.BP)

if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0")
