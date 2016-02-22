# -*- coding: utf-8 -*-

"""
In-memory copy of files in a given directory, updated when files are added or
updated.
"""

from __future__ import print_function
from os.path import join, abspath, isfile, getsize
from threading import Thread
from time import sleep
import os.path
import json
import os
# pylint: disable=W0312

################ Directory Cache ################
#
#
### What is the purpose of this: ###
#
# I wrote this as a simple in-memory copy of the files found on disk. All the
# files are read into memory at the beginning, and they're re-read into memory
# if they're modified, or if new files are added.
#
# There's a simple thread that is perpetually checking the directory and
# updating a data structure with the names and sizes of all files in the
# directory being cached. When it goes to read a file, it first checks that
# the in-memory data structure has all the same files as the updated
# structure, as well as checking that each in-memory file is the same size as
# the files in the updated structure. If there's a difference, it re-builds
# the entire cache then returns the requested data. If there's no difference,
# it just returns the requested data.
#
#
###     Why was this written:    ###
#
# I have a disk that can be extremely slow to seek to the start of a file.
# Sequential read and writes are fast, but reading a new file is frequently
# slow, and slow enough to notice. I wrote this so I could always read the
# data I wanted quickly, while also making sure that in-memory cache would be
# up to date if I changed a file or added a new file.
#
#
###            Notes:            ###
#
# This is the first time I've ever written anything like this. I don't know if
# there's some way to do this already, or if I could have done it better using
# some feature of python I'm not aware of. However, I'd love to learn about
# whatever mistakes or naive assumptions I've made in this code. If you do
# find something you think should be fixed, I'd really love to hear about it,
# either as a Github issue or as an email to me at lelandbatey@gmail.com
#
# Thanks for taking a look at all this, I hope it's useful/educational/humorous!
#
#  : )
#


def jdump(obj):
	"""Return json string representation of object"""
	return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

# Gets contents of a file
def get_file_contents(filename):
	"""Read a text file conveniently and properly."""
	ret_val = None
	with open(filename, 'r') as tmp_file:
		ret_val = tmp_file.read()
		if hasattr(ret_val, 'decode'):
			# python2 decode to utf-8
			ret_val = ret_val.decode('utf-8')
	return ret_val

def get_dir_files(path):
	"""Return list of files in directory."""
	data_dir = os.path.abspath(path)
	files = [f for f in os.listdir(data_dir) if isfile(join(data_dir, f))]
	return sorted(files)

def build_file_size_dir(path):
	"""Return dictionary of all files in a directory with their size."""
	return {f : getsize(join(path, f)) for f in get_dir_files(path)}


def strip_ext(files):
	"""Strips the extension from a filename or list of filenames"""
	if isinstance(files, list):
		# List comprehension of the above stripping process.
		return ['.'.join(f.split('.')[:-1]) for f in files]
	return '.'.join(files.split('.')[:-1])


class DirectoryCache(object):
	"""Cache of all files in root level of a directory.

	Only works with utf-8 encoded text files, since that's what I'm going to be
	dealing with.

	Initially loads the contents of a directory into memory, then spawns a
	thread that checks every half second if the contents of the underlying
	directory have been modified. If the on-disk contents have been modified,
	reloads them into memory. The check for updated files is done lazily, so
	only when attempting to access the cache.
	"""
	def __init__(self, data_dir):
		self.data_dir = data_dir
		self._cache = {}
		self.sizes_dict = {}

		# Used to watch the directory for changes in a non-blocking,
		# multi-threaded way.
		self.process_thread = Thread(target=self.build_file_size_dict)
		# Ensures that when the program dies, our thread dies as well.
		self.process_thread.daemon = True
		self.process_thread.start()

		self.build_cache()

	def get_files_list(self):
		"""Returns sorted list of files in the data_dir directory"""
		data_dir = os.path.abspath(self.data_dir)
		files = [f for f in os.listdir(data_dir) if isfile(join(data_dir, f))]
		return sorted(files)

	def build_file_size_dict(self):
		"""Rebuild the size of the directory."""
		# Every 0.5 seconds, re-evaluates the size of all the files in the
		# watched directory
		while True:
			self.sizes_dict = build_file_size_dir(self.data_dir)
			sleep(0.5)

	def is_cache_outdated(self):
		"""Returns True if the cache is outdated.

		The cache is considered outdated if any files have been added to the
		watched directory, or if any of the files within that directory differ
		in size from the cached version.
		"""
		current_state = self.sizes_dict
		current_cache = self._cache

		current_cache = {f : current_cache[f]['size'] for f in current_cache}

		for file_name in current_state:
			if file_name not in current_cache.keys():
				return True
			elif current_state[file_name] != current_cache[file_name]:
				return True

		return False

	def build_cache(self):
		"""Builds (or re-builds) the `self.cache` object"""
		t_cache = {}
		for file_name in self.get_files_list():
			path = abspath(join(self.data_dir, file_name))
			t_cache[file_name] = {'path'   : path,
			                      'data'   : get_file_contents(path),
			                      'no_ext' : strip_ext(file_name),
			                      'size'   : getsize(path)}
		self.cache = t_cache

	@property
	def cache(self):
		"""Returns existing cache or updates cache if outdated"""
		if self.is_cache_outdated():
			self.build_cache()
		return self._cache
	@cache.setter
	def cache(self, value):
		"""Return underlying cache object"""
		self._cache = value

	def __repr__(self):
		"""Return string version of directory cache"""
		return jdump(self.cache)

	def __getitem__(self, key):
		"""Implement dictionary-like access directly to the self.cache object"""
		return self.cache[key]

	def keys(self):
		"""Return the keys for underlying _cache object"""
		return self.cache.keys()
