from __future__ import print_function
import markdown
from os.path import join, abspath, isfile, basename
import os.path
import json
import os


def jsonDump(inDat):
	return json.dumps(inDat, sort_keys=True, indent=4, separators=(',', ': '))
def jp(inDat):
	print(jsonDump(inDat))

md = markdown.Markdown(safe_mode=False)

class flask_slides(object):
	"""Object for interacting with slides files"""
	def __init__(self, slides_dir=os.getcwd()+'/slides'):
		# super(flask_slides, self).__init__()
		self.slides_dir = slides_dir
		
	def get_slides(self):
		"""Returns dictionary of slide information for slides in slides_dir.

		Keys in the dictionary are the names of the slide files, with only the file extension removed.
		Values in the dict are the full paths to the slide files in the slides_dir.
		"""
		
		slides_dir = os.path.abspath(self.slides_dir)
		slides = [ f for f in os.listdir(slides_dir) if isfile(join(slides_dir, f))]

		# print(slides)
		toRet = {}

		for x in slides:
			toRet[self.strip_ext(x)] = abspath(join(self.slides_dir,x))

		# print(toRet)
		return toRet

	def render_slide(self, slide_name):
		"""Return string of rendered contents of the given slide.
		Valid slide names are 'slide_name' or 'slide_name.ext'

		If the slide exists, gets everything between the strings "<slide>" and "</slide>".
		If it doesn't exist, returns string "Does not exist".
		"""
		noneStr = "<h1>No data for that slide</h1>"
		slides = self.get_slides()

		# print(slide_name)
		# Check for slide short-names first
		for x in slides:
			# If name format is "slide_name"
			if self.strip_ext(basename(slides[x])) == slide_name:
				slide_path = slides[x]
				break
			# Else if name format is "slide_name.extension"
			elif basename(slides[x]) == slide_name:
				slide_path = slides[x]
				break

		slide = ""
		if isfile(slide_path):
			with open(slide_path, 'r') as f:
				slide = f.read()
				f.close()

			# Container tags allow for independant static viewing
			if '<slide>' in slide:
				slide = slide.split('<slide>')[1]
			if '</slide>' in slide:
				slide = slide.split('</slide>')[0]

		# If no slide was found, or if the slide was empty
		if not slide:
			slide = noneStr

		# Pass the slide through a markdown renderer. This preserves html, if
		# it's entered, but parses markdown into html. Allows for mixing of
		# the two.
		slide = markdown.markdown(slide, safe_mode=False)

		return slide

	def strip_ext(self, files):
		"""Given a file name or list of file names, strips the extension from each file name."""

		if   isinstance(files, basestring):
			return '.'.join(files.split('.')[:-1])
		elif isinstance(files, list):
			# List comprehension of the above stripping process.
			return [ '.'.join(f.split('.')[:-1]) for f in files ]






if __name__ == '__main__':
	f = flask_slides()
	jp(f.get_slides())
	exit()










