import io
from sampler import Sampler, FileFactory
import csv
import random
import os
import math
import sys

args = sys.argv[1:]
if len(args) != 5:
	print 'usage: python sample.py input-dir output-dir ../stats/foo.summary.psv quota.psv mbytes'
	sys.exit(1)
indir, outdir, summary, quota, mbytes = args

selected, total = Sampler(summary, FileFactory(indir)).get_files(quota, 1000000 * int(mbytes))
for file in selected:
	print file
	os.link(indir + '/' + file, outdir + '/' + file)
	yaml = os.path.splitext(file)[0] + '.yaml'
	if os.path.isfile(indir + '/' + yaml) and not os.path.isfile(outdir + '/' + yaml):
		os.link(indir + '/' + yaml, outdir + '/' + yaml)
