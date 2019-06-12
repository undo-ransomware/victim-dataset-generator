import requests
from lxml import etree
import re
from presentify import Presentation
from summarizer import extract_keywords, summarize
from mwclient import Site
import os
import io
from datetime import datetime
from slugify import slugify
from urllib import quote

wikipedia = Site('en.wikipedia.org')
commons = Site('commons.wikimedia.org')

def sectiontext(elem):
	return "".join(elem.xpath("*[not(@class) or @class!='mw-ref']//text()|text()"))

def convert(html, prs, metalog, source):
	xml = etree.fromstring(html)
	title = " ".join(xml.xpath("//title//text()"))
	prs.make_title(title, "From Wikipedia, the free encyclopedia", source,
		"Licensed unter CC BY-SA 3.0",
		"https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License");
	keywords = extract_keywords(xml.xpath("//section//text()"))
	
	for section in xml.xpath("//section"):
		headers = section.xpath("*[starts-with(name(),'h')]//text()")
		if len(headers) > 0:
			header = " ".join(headers)
		else:
			header = title
		
		for figure in section.xpath('figure'):
			caption = sectiontext(figure.xpath(".//figcaption")[0])
			src = re.sub('^.*?File:', '', figure.xpath(".//a//img/@resource")[0])

			basename, ext = os.path.splitext(src)
			localname = slugify(basename, max_length=150) + ext
			file = commons.images[src]
			meta = file.text()
			if '{{cc-zero' not in meta.lower() and '{{pd-' not in meta.lower():
				# we only use public-domain images to avoid dealing with attribution
				# or, worse, stuff that's only 
				continue
			if not os.path.isfile(localname):
				with open(localname, 'wb') as fd:
					file.download(fd)
			record_metadata(metalog, commons.host, src, file.text())
			summary = "".join(summarize([caption], keywords, 60))
			prs.make_image(localname, summary)
		
		text = [sectiontext(p) for p in section.xpath("p|ul/li|ol/li|dl/dt|dl/dd")]
		summary = summarize(text, keywords, 300)
		if len(summary) > 0:
			prs.make_bulleted(header, summary)

def record_metadata(metalog, site, filename, meta):
	metalog.write(u"source: " + site + "\n")
	metalog.write(u"file: " + filename + "\n")
	metalog.write(u"date: " + str(datetime.now()) + "\n")
	metalog.write(u"text: |\n")
	metalog.write(u"".join("  " + line for line in meta.splitlines(True)))
	metalog.write(u"\n---\n")

def download(page_title):
	prs = Presentation()
	with io.open(page_title + ".yaml", 'w', encoding='utf-8') as metalog:
		m = requests.get("https://en.wikipedia.org/api/rest_v1/page/title/" + page_title)
		record_metadata(metalog, wikipedia.host, page_title, m.text)
		r = requests.get("https://en.wikipedia.org/api/rest_v1/page/html/" + page_title)
		source = u"https://en.wikipedia.org/wiki/" + quote(page_title)
		convert(r.text, prs, metalog, source)
	prs.save(page_title + ".pptx")

def main(args):
	download(args[0])
	return 0
 
if __name__ == "__main__":
    import sys 
    status = main(sys.argv[1:])
    sys.exit(status)
