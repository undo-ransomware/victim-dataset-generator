import io
import csv

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

def add_file_rec(stats, reservoir, accum, depth, index):
	accumLeft = accum[depth][index]
	accumRight = accum[depth][index+1]
	accumTotal = accumLeft + accumRight + 1.0
	statsLeft = stats[depth][index]
	statsRight = stats[depth][index+1]
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
	if reservoir[depth][recurse] == 0:
		size = 2 ** depth
		print '!! need more stuff in bins', recurse * size, '..', (recurse + 1) * size - 1
		recurse ^= 1 # to the other side instead
		if reservoir[depth][recurse] == 0:
			raise Exception('...and the other side is empty as well!')
	accum[depth][recurse] += 1
	reservoir[depth][recurse] -= 1
	if depth == 0:
		print 'sampling bin', recurse
		# TODO actually pick a file
	else:
		add_file_rec(stats, reservoir, accum, depth - 1, 2 * recurse)

def add_file(stats, reservoir, accum, ext):
	add_file_rec(stats[ext], reservoir[ext], accum[ext], len(accum[ext]) - 1, 0)

stats = read_stats('../stats/uni.summary.psv')
accum = {'pdf':zero_tree()}
reservoir = {'pdf':[[1 for x in range(128)]]} # FIXME
build_tree(reservoir['pdf'])
for i in range(25):
	add_file(stats, reservoir, accum, 'pdf')
print reservoir, accum

# def main(args):
	# pass

#if __name__ == "__main__":
    # status = main(sys.argv[1:])
    # sys.exit(status)
