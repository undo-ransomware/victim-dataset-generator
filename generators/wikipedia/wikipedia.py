import requests
from lxml import etree
import io
import os
from datetime import datetime
from urllib import quote

LICENSE = "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"

def link(text, href, tail):
	a = etree.Element("a", href=href)
	a.text = text
	a.tail = tail
	return a

def download(page_title):
	if os.path.isfile('media/' + page_title + '.html'):
		return

	r = requests.get("https://en.wikipedia.org/api/rest_v1/page/html/" + quote(page_title))
	xml = etree.fromstring(r.text)
	rev = xml.xpath("/html/@about")[0]
	# remove external resources to keep pandoc from downloading them
	for fig in xml.xpath('//figure|//figure-inline|//img|//link[@rel="stylesheet"]|//script'):
		fig.xpath("..")[0].remove(fig)

	# attribution footer (to fulfill CC BY-SA)
	body = xml.xpath("//body")[0]
	body.append(etree.Element("hr"))
	p = etree.Element("p")
	p.append(link("From Wikipedia, the free encyclopedia",
		"https://en.wikipedia.org/wiki/" + quote(page_title),
		", and licensed under "))
	p.append(link("CC BY-SA 3.0", LICENSE, ". "))
	p.append(link("Version as of " + str(datetime.now()) + ".", rev, ""))
	body.append(p)

	with io.open('media/' + page_title + '.html', 'w', encoding='utf-8') as html:
		html.write(u"<!DOCTYPE html>")
		html.write(etree.tostring(xml).decode("utf-8"))

def main(args):
	for arg in args:
		download(arg)
	return 0

if __name__ == "__main__":
    import sys
    status = main(sys.argv[1:])
    sys.exit(status)
