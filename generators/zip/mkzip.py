import io
import os
import sys
import math
import subprocess
import random

class Files:
	def __init__(self, dir):
		self.src = dir
		self.files = [[] for x in range(128)]
		for file in os.listdir(dir):
			ext = os.path.splitext(file)[1][1:].lower()
			if ext == 'yaml':
				continue
			size = os.stat(dir + '/' + file).st_size
			if size == 0:
				print file, 'is empty!'
				continue
			
			dbb = int(round(10 * math.log10(size)))
			self.files[dbb].append((file, size))

	def sample(self, dbb):
		while len(self.files[dbb]) == 0:
			if dbb == 0:
				return None, 0
			dbb -= 1
		index = random.randrange(len(self.files[dbb]))
		return self.files[dbb].pop(index)

	def count(self, dbb):
		return len(self.files[dbb])

args = sys.argv[1:]
if len(args) < 4:
	print 'usage: python mkzip.py format input-dir output-dir bin...'
	sys.exit(1)
format, indir, outdir = args[0:3]
bins = args[3:]

for bin in bins:
	total_bytes = 10**(int(bin) / 10.0)
	files = Files(indir)
	bytes = 0
	selected = []
	while bytes < total_bytes:
		dbb = int(round(10 * math.log10(total_bytes - bytes))) - 2
		file, size = files.sample(dbb)
		if size == 0:
			break
		bytes += size
		selected.append(file)
	if len(selected) == 0:
		print 'cannot make', int(total_bytes), 'bytes of', format
		continue

	cmd = []
	if format == 'zip':
		cmd = ['zip', '-jq']
	elif format == 'rar':
		cmd = ['rar', 'a', '-ep']
	else:
		raise Exception('how do you make a ' + format + '?')
	while True:
		name = '-'.join(random.choice(os.path.splitext(file)[0].split('-')) for file in selected)[:100]
		outname = outdir + '/' + name + '.' + format
		if not os.path.isfile(outname):
			break
	cmd.append(outname)
	for file in selected:
		cmd.append(indir + '/' + file)
	subprocess.call(cmd)
	print 'made', outname, os.stat(outname).st_size, total_bytes
