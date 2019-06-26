import requests
from lxml import etree
import re
from presentify import Presentation
from wordify import TextDocument
from mwclient import Site
import os
import io
from datetime import datetime
from slugify import slugify
from urllib import quote, unquote
from tempfile import mkstemp
from PIL import Image
from resizeimage import resizeimage

commons = Site('commons.wikimedia.org')
LICENSE = "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"

def sectiontext(elem):
	return "".join(elem.xpath("*[not(@class) or @class!='mw-ref']//text()|text()"))

def convert(xml, sinks, metalog, source):
	title = " ".join(xml.xpath("//title//text()"))
	for sink in sinks:
		sink.make_title(title, "From Wikipedia, the free encyclopedia", source,
			"Licensed under CC BY-SA 3.0:", LICENSE);
		sink.init_full_text(xml.xpath("//section//text()"))
	
	for section in xml.xpath("//section"):
		headers = section.xpath("*[starts-with(name(),'h')]//text()")
		if len(headers) > 0:
			header = " ".join(headers)
		else:
			header = title
		
		for figure in section.xpath('figure|figure-inline'):
			caption = [sectiontext(c) for c in figure.xpath(".//figcaption")]
			res = figure.xpath(".//a//img/@resource")
			if len(res) == 0:
				continue
			src = unquote(re.sub('^.*?File:', '', res[0]))

			basename, ext = os.path.splitext(src)
			if ext.lower() in ['.svg', '.gif','.webp']:
				# SVG and WEBP is not supported by PIL
				# GIF tends to be animated, which invariably doesn't work
				continue
			localname = "cache/" + slugify(basename, max_length=150) + ext
			file = commons.images[src]
			meta = file.text()
			if '{{cc-zero' not in meta.lower() and '{{pd-' not in meta.lower():
				# we only use public-domain images to avoid dealing with attribution
				# or, worse, stuff that's only 
				continue
			if not os.path.isfile(localname):
				with open(localname, 'wb') as fd:
					file.download(fd)
			metalog.write(u"\n---\n")
			record_metadata(metalog, commons.host, src)
			metalog.write(u"text: |\n")
			metalog.write(u"".join("  " + line for line in file.text().splitlines(True)))
			temp = mkstemp(suffix=os.path.splitext(localname)[1])[1]
			with Image.open(localname) as img:
				resizeimage.resize_thumbnail(img, [1200, 750]).save(temp)
			for sink in sinks:
				sink.make_image(temp, caption)
			os.remove(temp)
		
		text = [sectiontext(p) for p in section.xpath("p|ul/li|ol/li|dl/dt|dl/dd")]
		for sink in sinks:
			sink.make_section(header, text)

def record_metadata(metalog, site, filename):
	metalog.write(u"source: " + site + "\n")
	metalog.write(u"file: " + filename.decode('utf-8') + "\n")
	metalog.write(u"date: " + str(datetime.now()) + "\n")

def download(page_title):
	if os.path.isfile('media/' + page_title + ".yaml"):
		return

	sinks = [Presentation(), TextDocument()]
	with io.open('media/' + page_title + ".yaml", 'w', encoding='utf-8') as metalog:
		r = requests.get("https://en.wikipedia.org/api/rest_v1/page/html/" + quote(page_title))
		xml = etree.fromstring(r.text)
		rev = xml.xpath("/html/@about")[0]
		record_metadata(metalog, "en.wikipedia.org", page_title)
		metalog.write(u"version: " + rev)
		source = u"https://en.wikipedia.org/wiki/" + quote(page_title)
		convert(xml, sinks, metalog, source)
	for sink in sinks:
		sink.save(page_title)

def main(args):
	for arg in args:
		download(arg)
	return 0
 
if __name__ == "__main__":
    import sys 
    status = main(sys.argv[1:])
    sys.exit(status)
