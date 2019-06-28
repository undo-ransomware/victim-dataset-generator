import io
import csv
import random
import os
import math
import sys

from mime_map import mimetypes

args = sys.argv[1:]
if len(args) == 0:
	print 'usage: python stats.py directoy...'
	sys.exit(1)

files = dict()
def recurse(dir):
	for file in os.listdir(dir):
		file = dir + '/' + file
		if os.path.isdir(file):
			recurse(file)
		if not os.path.isfile(file):
			continue

		ext = os.path.splitext(file)[1][1:].lower()
		if len(ext) > 4:
			ext = '...'

		size = os.stat(dir + '/' + file).st_size
		if size == 0:
			dbb = -1
		else:
			dbb = int(round(10 * math.log10(size)))

		if ext not in files:
			files[ext] = dict()
		if dbb not in files[ext]:
			files[ext][dbb] = 0
		files[ext][dbb] += 1

for dir in args:
	recurse(dir)

print 'mimetype|dbb|count|ext'
for ext in files.keys():
	if ext in mimetypes:
		mime = mimetypes[ext]
	else:
		mime = 'application/octet-stream'
	for dbb in files[ext].keys():
		print mime + '|' + str(dbb) + '|' + str(files[ext][dbb]) + '|' + ext
