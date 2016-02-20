# -*- coding: utf-8 -*-
"""An API for interacting with the slides stored in the `slides/` directory."""

from __future__ import print_function
from os.path import join, abspath
import directory_cache
from directory_cache import strip_ext, jdump
import markdown
import os.path
import json
import os
# pylint: disable=W0312


################  Flask_Slides   ################
#
#
###             What:            ###
#
# Flask_slides takes the simple model of slides as files in a directory and
# gives it an API. This is to make programatically loading and navigating the
# slides easier.
#
#
###             Why:             ###
#
# Because it would have been a pain (and messy!) to implement all this in the
# `app.py` file. This way, `app.py` just does http/Flask stuff, and the
# handling the slides is done over here.
#


def jprint(obj):
	"""Print a json representation of a given object"""
	print(jdump(obj))


class FlaskSlides(object):
	"""Object for interacting with slides files"""
	def __init__(self, slides_dir=os.getcwd()+'/slides'):
		# super(flask_slides, self).__init__()
		self.slides_dir = slides_dir
		self._index = 0
		self.invalid_slide = "<h1>No data for that slide</h1>"
		self.cache = directory_cache.DirectoryCache(self.slides_dir)


	def get_slide_list(self):
		"""Returns sorted list of slides in the slide directory"""
		return self.cache.get_files_list()

	def get_slides(self):
		"""Returns dictionary of slide information for slides in slides_dir.

		Keys in the dictionary are the names of the slide files, with only the
		file extension removed.  Values in the dict are the full paths to the
		slide files in the slides_dir.
		"""
		slides = self.get_slide_list()
		ret_val = {}

		for slide in slides:
			ret_val[strip_ext(slide)] = abspath(join(self.slides_dir, slide))

		return ret_val

	def render_slide(self, slide_name):
		"""Return string of rendered contents of the given slide.
		Valid slide names are 'slide_name' or 'slide_name.ext'

		If the slide exists, gets everything between the strings "<slide>" and
		"</slide>".  If it doesn't exist, returns string "Does not exist".
		"""

		slides = self.get_slides()
		slide_path = ""
		slide = ""

		# Try to match the given slide to the path of the actual file
		for _ in slides:
			# If name format is "slide_name.extension"
			if slide_name in self.cache.keys():
				slide_path = self.cache[slide_name]
				break
			# Else if name format is "slide_name"
			else:
				for k in self.cache.keys():
					if self.cache[k]['no_ext'] == slide_name:
						slide_path = k
						break
				if slide_path:
					break

		if slide_path:
			# Get contents of slide
			slide = self.cache[slide_path]['data']

			# Container tags allow for independant static viewing
			if '<slide>' in slide:
				slide = slide.split('<slide>')[1]
			if '</slide>' in slide:
				slide = slide.split('</slide>')[0]

		# If no slide was found, or if the slide was empty
		if not slide:
			slide = self.invalid_slide

		extension = ['codehilite(css_class=highlight,linenums=True)']
		# Pass the slide through a markdown renderer. This preserves html, if
		# it's entered, but parses markdown into html. Allows for mixing of
		# the two.
		slide = markdown.markdown(slide, safe_mode=False, extensions=extension)

		return slide

	def render_index(self, slide_number):
		"""Given an index, render that slide (in the series of slides)."""
		self.index = slide_number
		slide_list = sorted(self.get_slides())
		for idx, value in enumerate(slide_list):
			if idx == slide_number:
				return self.render_slide(value)

		return self.invalid_slide

	# Creating properties for index so we can keep it from dropping below 0 or
	# going beyond the number of total slides.
	@property
	def index(self):
		"""Return value of underlying index value"""
		return self._index
	@index.setter
	def index(self, value):
		"""Set index as property.
		
		Done so index is always greater than 0 or less than the total number of
		slides.
		"""
		slide_count = len(self.get_slide_list())-1
		if value < 0:
			self._index = 0
		elif value > slide_count:
			self._index = slide_count
		else:
			self._index = value


if __name__ == '__main__':
	jprint(flask_slides().get_slides())

