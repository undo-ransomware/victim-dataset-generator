import requests
from lxml import etree
import io
from datetime import datetime
from urllib import quote

LICENSE = "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"

def link(text, href, tail):
	a = etree.Element("a", href=href)
	a.text = text
	a.tail = tail
	return a

def download(page_title):
	with io.open(page_title + ".yaml", 'w', encoding='utf-8') as metalog:
		r = requests.get("https://en.wikipedia.org/api/rest_v1/page/html/" + page_title)
		xml = etree.fromstring(r.text)
		rev = xml.xpath("/html/@about")[0]
		metalog.write(u"source: en.wikipedia.org\n")
		metalog.write(u"file: " + page_title + "\n")
		metalog.write(u"date: " + str(datetime.now()) + "\n")
		metalog.write(u"version: " + rev)
		header = etree.Element("h1")
		header.text = page_title
		xml.insert(0, header)

		xml.append(etree.Element("hr"))
		p = etree.Element("p")
		p.append(link("From Wikipedia, the free encyclopedia",
			"https://en.wikipedia.org/wiki/" + quote(page_title),
			", and licensed under "))
		p.append(link("CC BY-SA 3.0", LICENSE, "."))
		xml.append(p)
		with io.open(page_title + ".html", 'w', encoding='utf-8') as html:
			html.write(etree.tostring(xml).decode("utf-8"))

def main(args):
	for arg in args:
		download(arg)
	return 0

if __name__ == "__main__":
    import sys
    status = main(sys.argv[1:])
    sys.exit(status)
