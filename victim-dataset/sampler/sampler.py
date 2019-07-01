import io
import csv
import random
import os
import math
import sys
import importlib

BINS = 128
DEPTH = 6

def init_tree():
	return [[0 for x in range(BINS)]]

def fill_tree(tree):
	for i in range(DEPTH):
		tree.append([tree[i][j] + tree[i][j+1] for j in range(0, len(tree[i])-1, 2)])

class Sampler:
	def __init__(self, stats_filename, files, quota_module):
		self.files = files
		self.stats = dict()
		with io.open(stats_filename, 'r') as file:
			for row in csv.DictReader(file, delimiter='|'):
				ext = row['ext']
				if ext not in self.stats:
					self.stats[ext] = init_tree()
				dbb = int(row['dbb'])
				self.stats[ext][0][dbb] = int(row['count'])

		self.reservoir = dict((ext, [[self.files.count(ext, dbb) for dbb in range(BINS)]])
				for ext in self.stats.keys())
		self.accum = dict((ext, init_tree()) for ext in self.stats.keys())
		for ext in self.stats.keys():
			fill_tree(self.stats[ext])
			fill_tree(self.reservoir[ext])
			fill_tree(self.accum[ext])

		self.quota = dict()
		importlib.import_module(quota_module).quota(self)

	def combine(self, *exts):
		total = init_tree();
		fill_tree(total)
		for depth in range(len(total)):
			for dbb in range(len(total[depth])):
				total[depth][dbb] = sum(self.stats[ext][depth][dbb] for ext in exts)
		for ext in exts:
			self.stats[ext] = total

	def sample(self, ext, class_fraction, type_fraction):
		self.quota[ext] = class_fraction * type_fraction

	def get_file(self, ext, limit):
		depth = DEPTH
		index = 0
		while True:
			accumLeft = self.accum[ext][depth][index]
			accumRight = self.accum[ext][depth][index+1]
			accumTotal = accumLeft + accumRight + 1.0
			statsLeft = self.stats[ext][depth][index]
			statsRight = self.stats[ext][depth][index+1]
			statsTotal = float(statsLeft + statsRight)
			def error(left, right):
				return abs(statsLeft / statsTotal - left / accumTotal) + abs(statsRight / statsTotal - right / accumTotal)
			errorLeft = error(accumLeft + 1, accumRight)
			errorRight = error(accumLeft, accumRight + 1)

			size = 2 ** depth
			#print >> sys.stderr, 'recurse', depth, index, 'left', accumLeft, statsLeft, errorLeft, 'right', accumRight, statsRight, errorRight, 'limit', limit, (index + 1) * size
			recurse = -1
			if errorLeft < errorRight or (index + 1) * size > limit:
				recurse = index
				if statsLeft == 0:
					print >> sys.stderr, '!! cannot sample', ext, 'from empty bins', recurse * size, '..', (recurse + 1) * size - 1
					return (None, None)
				#print >> sys.stderr, 'to the left', index, recurse
			else:
				recurse = index + 1
				#print >> sys.stderr, 'to the right', index, recurse
			if self.reservoir[ext][depth][recurse] == 0:
				print >> sys.stderr, '!! need more', ext, 'in bins', recurse * size, '..', (recurse + 1) * size - 1
				recurse ^= 1 # to the other side instead
				if self.reservoir[ext][depth][recurse] == 0:
					# both sides empty, so parent node should be empty, so this should
					# have been detected before the recursive call.
					raise Exception('...and the other side is empty as well!')
			self.accum[ext][depth][recurse] += 1
			self.reservoir[ext][depth][recurse] -= 1
			if depth == 0:
				file, bytes = self.files.sample(ext, recurse)
				print >> sys.stderr, 'sampling bin', recurse, file, bytes
				return (file, bytes)
			depth = depth - 1
			index = 2 * recurse

	def get_files_for_ext(self, ext, max_bytes):
		bytes = 0
		selected = []
		while bytes < max_bytes:
			limit = 10 * math.log10(max_bytes - bytes)
			file, size = self.get_file(ext, limit)
			if file is None:
				break
			bytes += size
			selected.append(file)
		return (selected, bytes)

	def get_files(self, max_bytes):
		selected = []
		total = 0
		for ext in self.quota.keys():
			files, bytes = self.get_files_for_ext(ext, self.quota[ext] * max_bytes)
			total += bytes
			selected.append(files)
		return [f for fs in selected for f in fs], total

class FileFactory:
	def __init__(self, dir):
		self.files = dict()
		for file in os.listdir(dir):
			ext = os.path.splitext(file)[1][1:].lower()
			if ext == 'yaml':
				continue
			size = os.stat(dir + '/' + file).st_size
			if size == 0:
				print >> sys.stderr, file, 'is empty!'
				continue

			dbb = int(round(10 * math.log10(size)))
			if ext not in self.files:
				self.files[ext] = [[] for x in range(BINS)]
			self.files[ext][dbb].append((file, size))

	def sample(self, ext, dbb):
		index = random.randrange(len(self.files[ext][dbb]))
		return self.files[ext][dbb].pop(index)

	def count(self, ext, dbb):
		if ext not in self.files:
			return 0
		return len(self.files[ext][dbb])
