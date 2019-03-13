import requests
import re
import shutil
import sys
import time
from mwclient import Site
from slugify import slugify
import os

site = Site('commons.wikimedia.org')

def download_random_file():
	r = requests.get("https://commons.wikimedia.org/wiki/Special:Random/File")
	d = re.search('(?<=<title>File:).+?(?= - Wikimedia Commons</title>)', r.text, re.DOTALL)
	file = site.images[d.group()]
	with open('./media/' + d.group(), 'wb') as fd:
		print 'Downloading: ' + d.group().encode(sys.stdout.encoding, errors='replace')
		file.download(fd)
	time.sleep(1)
	
def download_category_files(category_name):
	category_name = "Audio_files_of_music"
	category = site.Categories[category_name]
	for x in category.members(namespace=6):
		file = site.images[x.page_title]
		filename, extension = os.path.splitext(x.page_title)
		with open('./media/' + slugify(filename) + extension, 'wb') as fd:
			print 'Downloading: ' + slugify(filename) + extension
			file.download(fd)
		time.sleep(1)
	
def main(args):
	if args[0] == 'random':
		print 'Downloading ' + args[1] + ' random files.'
		for i in range(int(args[1])):
			download_random_file()
	elif args[0] == 'category':
		print 'Downloading the ' + args[1] + ' category.'
		download_category_files(args[1])
	else:
		print "<random|category> <number of random files|wikimedia category>"
 
if __name__ == "__main__":
    status = main(sys.argv[1:])
    sys.exit(status)