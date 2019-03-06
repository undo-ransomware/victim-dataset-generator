import requests
import re
import shutil
import sys
import time


for i in range(100):
	r = requests.get("https://en.wikipedia.org/wiki/Special:Random")
	d = re.search('(?<=<title>).+?(?= - Wikipedia</title>)', r.text, re.DOTALL)
	print d.group().encode(sys.stdout.encoding, errors='replace')
	response = requests.get('https://en.wikipedia.org/api/rest_v1/page/pdf/' + d.group(), stream=True)
	with open('./pdf/' + d.group() + ".pdf", 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	time.sleep(1)