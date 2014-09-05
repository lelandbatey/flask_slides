from __future__ import print_function
import markdown
from os.path import join, abspath, isfile, basename, getsize
from time import sleep
import directory_cache
import os.path
import json
import os

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


def jsonDump(inDat):
	return json.dumps(inDat, sort_keys=True, indent=4, separators=(',', ': '))
def jp(inDat):
	print(jsonDump(inDat))

def strip_ext(files):
	"""Given a file name or list of file names, strips the extension from each file name."""
	if   isinstance(files, basestring):
		return '.'.join(files.split('.')[:-1])
	elif isinstance(files, list):
		# List comprehension of the above stripping process.
		return [ '.'.join(f.split('.')[:-1]) for f in files ]



class flask_slides(object):
	"""Object for interacting with slides files"""
	def __init__(self, slides_dir=os.getcwd()+'/slides'):
		# super(flask_slides, self).__init__()
		self.slides_dir = slides_dir
		self._index = 0
		self.noneStr = "<h1>No data for that slide</h1>"
		self.cache = directory_cache.directory_cache(self.slides_dir)
		

	def get_slide_list(self):
		"""Returns sorted list of slides in the slide directory"""
		return self.cache.get_files_list()
		
	def get_slides(self):
		"""Returns dictionary of slide information for slides in slides_dir.

		Keys in the dictionary are the names of the slide files, with only the file extension removed.
		Values in the dict are the full paths to the slide files in the slides_dir.
		"""
		slides = self.get_slide_list()
		toRet = {}

		for x in slides:
			toRet[strip_ext(x)] = abspath(join(self.slides_dir,x))

		return toRet

	def render_slide(self, slide_name):
		"""Return string of rendered contents of the given slide.
		Valid slide names are 'slide_name' or 'slide_name.ext'

		If the slide exists, gets everything between the strings "<slide>" and "</slide>".
		If it doesn't exist, returns string "Does not exist".
		"""
		
		slides = self.get_slides()
		slide_path = ""
		slide = ""

		# Try to match the given slide to the path of the actual file
		for x in slides:
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
				if slide_path: break

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
			slide = self.noneStr

		# Pass the slide through a markdown renderer. This preserves html, if
		# it's entered, but parses markdown into html. Allows for mixing of
		# the two.
		slide = markdown.markdown(slide, safe_mode=False, extensions=['codehilite(css_class=highlight,linenums=True)'])

		return slide

	def render_index(self, slide_number):
		"""Given an index, render that slide (in the series of slides)."""
		self.index = slide_number
		i = 0
		slide_list = sorted(self.get_slides())
		for x in slide_list:
			if i == slide_number:
				return self.render_slide(x)
			i += 1

		return self.noneStr

	# Creating properties for index so we can keep it from dropping below 0 or
	# going beyond the number of total slides.
	@property
	def index(self):
		return self._index
	@index.setter
	def index(self, value):
		slide_count = len(self.get_slide_list())-1
		if value < 0:
			self._index = 0
		elif value > slide_count:
			self._index = slide_count
		else:
			self._index = value


if __name__ == '__main__':
	f = flask_slides()
	jp(f.get_slides())











