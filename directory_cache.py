from __future__ import print_function
from os.path import join, abspath, isfile, basename, getsize
from threading import Thread
from time import sleep
import os.path
import time
import json
import os


def jsonDump(inDat):
	return json.dumps(inDat, sort_keys=True, indent=4, separators=(',', ': '))
def jp(inDat):
	print(jsonDump(inDat))

# Gets contents of a file
def get_file_contents(file_name):
	with open(file_name, 'r') as f: toRet = f.read().decode('utf-8')
	return toRet

def get_dir_files(path):
	data_dir = os.path.abspath(path)
	files = [ f for f in os.listdir(data_dir) if isfile(join(data_dir, f))]
	return sorted(files)

def build_file_size_dir(path):
	return {f : getsize(join(path,f)) for f in get_dir_files(path)}


def strip_ext(files):
	"""Given a file name or list of file names, strips the extension from each file name."""
	if   isinstance(files, basestring):
		return '.'.join(files.split('.')[:-1])
	elif isinstance(files, list):
		# List comprehension of the above stripping process.
		return [ '.'.join(f.split('.')[:-1]) for f in files ]


class directory_cache(object):
	"""Cache of all files in root level of a directory.

	Only works with utf-8 encoded text files, since that's what I'm going to be dealing with.
	"""
	def __init__(self, data_dir):
		# super(directory_cache, self).__init__()
		self.data_dir = data_dir
		self._cache = {}
		self.sizes_dict = {}


		# Used to watch the directory for changes in a non-blocking, multi-threaded way
		self.procThread = Thread(target=self.build_file_size_dict)
		self.procThread.daemon = True # When the program dies, our thread dies as well.
		self.procThread.start()

		self.build_cache()

	def get_files_list(self):
		"""Returns sorted list of files in the data_dir directory"""
		data_dir = os.path.abspath(self.data_dir)
		files = [ f for f in os.listdir(data_dir) if isfile(join(data_dir, f))]
		return sorted(files)
		
	def build_file_size_dict(self):
		# Every 0.5 seconds, re-evaluates the size of all the files in the watched directory
		while True:
			self.sizes_dict = build_file_size_dir(self.data_dir)
			# jp(self.sizes_dict)
			# print(time.time())
			sleep(0.5)

	def is_cache_outdated(self):
		"""Returns True if the cache is outdated.

		The cache is considered outdated if any files have been added to the
		watched directory, or if any of the files within that directory differ
		in size from the cached version.

		"""
		current_state = self.sizes_dict
		current_cache = self._cache

		current_cache = { f : current_cache[f]['size'] for f in current_cache }

		for x in current_state:
			if x not in current_cache.keys():
				return True
			elif current_state[x] != current_cache[x]:
				return True

		return False

	def build_cache(self):
		"""Builds (or re-builds) the `self.cache` object"""
		t_cache = {}
		for x in self.get_files_list():
			path = abspath(join(self.data_dir,x))
			t_cache[x] = {
				'path'   : path,
				'data'   : get_file_contents(path),
				'no_ext' : strip_ext(x),
				'size'   : getsize(path)
			}
		self.cache = t_cache

	@property
	def cache(self):
		if self.is_cache_outdated():
			self.build_cache()
		return self._cache
	@cache.setter
	def cache(self, value):
		self._cache = value

	def __repr__(self):
		return jsonDump(self.cache)

	def __getitem__(self, key):
		# Allows for dictionary-like access directly to the self.cache item
		return self.cache[key]

	def keys(self):
		return self.cache.keys()