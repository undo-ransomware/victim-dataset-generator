import requests
import re
import shutil
import sys
import time
from mwclient import Site
from mwclient.listing import List
from slugify import slugify
import os
import random
import string
from lxml import etree
import json
import urllib
from datetime import datetime
import io

site = Site('commons.wikimedia.org')

def download(filename):
	file = site.images[filename]
	basename, extension = os.path.splitext(filename)
	localname = slugify(basename, max_length=150)
	print 'Downloading to: ' + localname + extension
	with io.open('./media/' + localname + ".yaml", 'w', encoding='utf-8') as fd:
		fd.write(u"source: " + site.host + "\n")
		fd.write(u"file: " + filename + "\n")
		fd.write(u"date: " + str(datetime.now()) + "\n")
		fd.write(u"text: |\n")
		fd.write(u"".join("  " + line for line in file.text().splitlines(True)))
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
	# screenscrape the category frontend since the API doesn't offer a way to randomly
	# sample a category. fully downloading the category using the API and then sampling
	# locally would work, but for large categories like CC-Zero would create more load
	# than screenscraping.
	start = ''.join(random.choice(string.ascii_lowercase) for x in range(0,10))
	r = requests.get("https://commons.wikimedia.org/wiki/Category:" + category_name + "?from=" + start)
	xml = etree.fromstring(r.text)
	href = xml.xpath('//div[@id="mw-category-media"]//a[@class="image"]/@href')
	d = re.search('(?<=/wiki/File:).+?$', random.choice(href), re.DOTALL)
	file = urllib.unquote(d.group()).decode("utf-8")
	download(file)

def download_search_files(query):
	for res in List(site, 'search', 'sr', srsearch=query, srnamespace=6, srprop='', srsort='none'):
		download(re.sub('^File:', '', res['title']))

def download_search_random(query, count):
	q = site.get('query', list='search', srsearch=query, srlimit=1, srprop='', srsort='none', srnamespace=6)
	total = q['query']['searchinfo']['totalhits']
	if total > 10000:
		print "Limiting sampling to first 10k results of " + str(total)
		total = 10000
	else:
		print "Sampling " + str(total) + " results"
	for i in range(count):
		index = random.randrange(total)
		l = List(site, 'search', 'sr', limit=1, sroffset=index, srsearch=query, srnamespace=6, srprop='', srsort='none')
		title = l.next()['title']
		download(re.sub('^File:', '', title))

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
	elif args[0] == 'search':
		print 'Downloading all files matching ' + args[1]
		download_search_files(args[1])
	elif args[0] == 'randomsearch':
		print 'Downloading ' + args[2] + ' files matching ' + args[1]
		download_search_random(args[1], int(args[2]))
	else:
		print "random <number of random files>"
		print "category <wikimedia category>"
		print "randomcat <number of random files> <wikimedia category>"
		print "search <search query>"
		print "randomsearch <number of random files> <search query>"

if __name__ == "__main__":
    status = main(sys.argv[1:])
    sys.exit(status)
