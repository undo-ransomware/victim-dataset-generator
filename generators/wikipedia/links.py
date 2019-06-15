from mwclient import Site

site = Site("en.wikipedia.org")

def list(page_title):
	for link in site.pages[page_title].links(namespace=0, generator=False):
		print link.encode("utf-8")

def main(args):
	for arg in args:
		list(arg)
	return 0

if __name__ == "__main__":
    import sys
    status = main(sys.argv[1:])
    sys.exit(status)
