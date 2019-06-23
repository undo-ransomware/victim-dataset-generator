import io
import csv
import random
import os
import math
import sys

def init_tree():
	return [[0 for x in range(128)]]

def build_tree(tree):
	for i in range(6):
		tree.append([tree[i][j] + tree[i][j+1] for j in range(0, len(tree[i])-1, 2)])

def zero_tree():
	tree = init_tree()
	build_tree(tree)
	return tree

def read_stats(filename):
	stats = dict()
	with io.open(filename, 'r') as file:
		for row in csv.DictReader(file, delimiter='|'):
			ext = row['ext']
			if ext not in stats:
				stats[ext] = init_tree()
			dbb = int(row['dbb'])
			stats[ext][0][dbb] = int(row['count'])
	
	for ext in stats.keys():
		build_tree(stats[ext])
	return stats

def scan_files(dir):
	reservoir = dict((ext, init_tree()) for ext in stats.keys())
	files = dict((ext, [[] for x in range(128)]) for ext in stats.keys())

	for file in os.listdir(dir):
		ext = os.path.splitext(file)[1][1:].lower()
		if ext == 'yaml':
			continue
		size = os.stat(dir + '/' + file).st_size
		if size == 0:
			print file, 'is empty!'
			continue
		
		dbb = int(round(10 * math.log10(size)))
		reservoir[ext][0][dbb] += 1
		files[ext][dbb].append(file)

	for ext in stats.keys():
		build_tree(reservoir[ext])
	return reservoir, files

def add_file_rec(ext, depth, index):
	accumLeft = accum[ext][depth][index]
	accumRight = accum[ext][depth][index+1]
	accumTotal = accumLeft + accumRight + 1.0
	statsLeft = stats[ext][depth][index]
	statsRight = stats[ext][depth][index+1]
	statsTotal = float(statsLeft + statsRight)
	def error(left, right):
		return abs(statsLeft / statsTotal - left / accumTotal) + abs(statsRight / statsTotal - right / accumTotal)
	errorLeft = error(accumLeft + 1, accumRight)
	errorRight = error(accumLeft, accumRight + 1)
	
	#print 'recurse', depth, index, 'left', accumLeft, statsLeft, errorLeft, 'right', accumRight, statsRight, errorRight
	recurse = -1
	if errorLeft < errorRight:
		recurse = index
		#print 'to the left', index, recurse
	else:
		recurse = index + 1
		#print 'to the right', index, recurse
	if reservoir[ext][depth][recurse] == 0:
		size = 2 ** depth
		print '!! need more', ext, 'in bins', recurse * size, '..', (recurse + 1) * size - 1
		recurse ^= 1 # to the other side instead
		if reservoir[ext][depth][recurse] == 0:
			# both sides empty, so parent node should be empty, so this should
			# have been detected before the recursive call.
			raise Exception('...and the other side is empty as well!')
	accum[ext][depth][recurse] += 1
	reservoir[ext][depth][recurse] -= 1
	if depth == 0:
		index = random.randrange(len(files[ext][recurse]))
		file = files[ext][recurse].pop(index)
		print 'sampling bin', recurse, file
		return file, 10**(recurse/10.0)
	else:
		return add_file_rec(ext, depth - 1, 2 * recurse)

def add_file(ext):
	return add_file_rec(ext, len(accum[ext]) - 1, 0)

def add_files(ext, max_files, max_bytes):
	bytes = 0
	selected = []
	while len(selected) < max_files and bytes < max_bytes:
		file, size = add_file(ext)
		bytes += size
		selected.append(file)
	return selected

args = sys.argv[1:]
if len(args) != 3:
	print 'usage: python sample.py ../stats/foo.summary.psv output-dir quota.psv'
	sys.exit(1)
stats = read_stats(args[0])
accum = dict((ext, zero_tree()) for ext in stats.keys())
reservoir, files = scan_files('media')
with io.open(args[2], 'r') as file:
	for row in csv.DictReader(file, delimiter='|'):
		selected = add_files(row['ext'], int(row['max_files']), 1e6 * float(row['max_mbytes']))
		for file in selected:
			yaml = os.path.splitext(file)[0] + '.yaml'
			os.link('media/' + file, args[1] + '/' + file)
			os.link('media/' + yaml, args[1] + '/' + yaml)
