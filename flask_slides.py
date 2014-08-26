from __future__ import print_function
import markdown
from os.path import join, abspath, isfile
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
		"""Return dictionary of slide information for slides in slides_dir.

		Keys in the dictionary are the names of the slide files, with only the file extension removed.
		Values in the dict are the full paths to the slide files in the slides_dir.
		"""
		
		slides_dir = os.path.abspath(self.slides_dir)
		slides = [ f for f in os.listdir(slides_dir) if isfile(join(slides_dir, f))]

		# print(slides)
		toRet = {}

		for x in slides:
			toRet['.'.join(x.split('.')[:-1])] = abspath(join(self.slides_dir,x))

		return toRet

	def render_slide(self, slide_name):
		"""Return string of rendered contents of the given slide.

		If the slide exists, gets everything between the strings "<slide>" and "</slide>".
		If it doesn't exist, returns string "Does not exist".
		"""
		noneStr = "<h1>No data for that slide</h1>"
		slide_path = abspath(join(self.slides_dir, slide_name))

		slide = ""
		if isfile(slide_path):
			with open(slide_path, 'r') as f:
				slide = f.read()

			if '<slide>' in slide:
				slide = slide.split('<slide>')[1]
			if '</slide>' in slide:
				slide = slide.split('</slide>')[0]

		# If no slide was found, or if the slide was empty
		if not slide:
			slide = noneStr

		# Pass the slide through a markdown renderer. This preserves html, if it's entered, but parses it as 
		slide = markdown.markdown(slide, safe_mode=False)

		return slide






if __name__ == '__main__':
	f = flask_slides()
	jp(f.get_slides())
	exit()










