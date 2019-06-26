import requests
from time import sleep

WIKI = 'https://en.wikipedia.org/wiki/'

def get_random_page():
	r = requests.get(WIKI + 'Special:Random', allow_redirects=False)
	if r.status_code != 302:
		raise Exception('response status: ' + r.status_code)
	location = r.headers['Location']
	if not location.startswith(WIKI):
		raise Exception('redirect to: ' + location)
	return location[len(WIKI):]

def main(args):
	for i in range(int(args[0])):
		print get_random_page()
		sleep(1)
	return 0

if __name__ == "__main__":
    import sys
    status = main(sys.argv[1:])
    sys.exit(status)
