import requests
import re
import shutil
import sys
import time
from mwclient import Site
from slugify import slugify
import os
import random
import string
from lxml import etree
import json
import urllib

site = Site('commons.wikimedia.org')

def download(filename):
	file = site.images[filename]
	basename, extension = os.path.splitext(filename)
	localname = slugify(basename, max_length=150)
	print 'Downloading to: ' + localname + extension
	with open('./media/' + localname + extension, 'wb') as fd:
		file.download(fd)
	time.sleep(1)

def download_random_file():
	r = requests.get("https://commons.wikimedia.org/wiki/Special:Random/File")
	d = re.search('(?<=<title>File:).+?(?= - Wikimedia Commons</title>)', r.text, re.DOTALL)
	download(d.group())
	
def download_category_files(category_name):
	category = site.Categories[category_name]
	for x in category.members(namespace=6):
		download(x.page_title)
	
def download_category_random(category_name):
	start = ''.join(random.choice(string.ascii_lowercase) for x in range(0,10))
	r = requests.get("https://commons.wikimedia.org/wiki/Category:" + category_name + "?from=" + start)
	xml = etree.fromstring(r.text)
	href = xml.xpath('//div[@id="mw-category-media"]//a[@class="image"]/@href')
	d = re.search('(?<=/wiki/File:).+?$', random.choice(href), re.DOTALL)
	file = urllib.unquote(d.group()).decode("utf-8")
	download(file)
	
def main(args):
	if args[0] == 'random':
		print 'Downloading ' + args[1] + ' random files.'
		for i in range(int(args[1])):
			download_random_file()
	elif args[0] == 'category':
		print 'Downloading the ' + args[1] + ' category.'
		download_category_files(args[1])
	elif args[0] == 'randomcat':
		print 'Downloading ' + args[2] + ' files from the ' + args[1] + ' category.'
		for i in range(int(args[2])):
			download_category_random(args[1])
	else:
		print "random <number of random files>"
		print "category <wikimedia category>"
		print "randomcat <number of random files> <wikimedia category>"
 
if __name__ == "__main__":
    status = main(sys.argv[1:])
    sys.exit(status)
