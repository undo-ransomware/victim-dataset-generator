import requests
import json
import time
import sys
import io
import random
from zipfile import ZipFile

# pulls data from https://factfinder.census.gov/
# because that's the US federal government, the data is in the public domain.

SITE = 'https://factfinder.census.gov'
DOWNLOAD = SITE + '/rest/downloadRequest'
TABLE = SITE + '/tablerestful/tableServices'

def download(session, info):
	# they probably have an API, but this was easier
	product_key = info['p_product_key']
	print 'Downloading ' + product_key
	rnd = str(int(time.time() * 1000))
	ts = str(int(rnd) - 981954000) # 2001-02-12, 06:00:00... wtf?!
	# select the table
	infokey = '|'.join([product_key, 'table', '', '', '', #info['p_record_spec'],
		info['p_product_code'], info['p_record_name']])
	session.post(TABLE + '/productSelection', data={'log': 'f', 'prodsA': infokey, '_ts': ts})
	# select data by County (this takes forever because it also returns search data)
	session.post(SITE + '/rest/geoSearch/geoassist',
		data={'log': 't', 'src': 'geoassist', 'param': 'geo', 'ga.summaryLevel': '050',
			'selections':'All Counties within United States and Puerto Rico~County~050~2018'})
	session.get(TABLE + '/renderProductData?renderForMap=f&renderForChart=f&pid=' +
		product_key + '&log=t&_ts=' + ts)
	# get a download slot and start download
	rid = json.loads(session.get(DOWNLOAD + '/init?rnd=' + rnd).text)['reservationId']
	if rid is None:
		raise Exception('init failed')
	session.get(DOWNLOAD + '/construct?reservationId=' + rid +
		'&context=TABLE&disposition=ATTACHMENT&packagingFormat=BUNDLED&aggregation=SINGLE' +
		'&reportFormat=CSV&requestType=DB_COMPATIBLE&dataAndAnnotationsInSingleFile=true' +
		'&includeDescDataElements=true&log=t&_ts=' + ts)
	# poll for completion
	status = None
	while status != 'COMPLETED':
		poll = session.get(DOWNLOAD + '/status?reservationId=' + rid + '&rnd=' + rnd)
		status = json.loads(poll.text)['downloadRequestStatus']
		if status == 'CANCELED':
			raise Exception('download cancelled')
		print status
		time.sleep(1)
	# and finally, download file to disk and unpack
	data = session.get(DOWNLOAD + '/deliver?reservationId=' + rid + '&_ts=' + ts)
	zipfile = "zips/" + product_key + '-' + rid + '.zip'
	with io.open(zipfile, 'wb') as zip:
		zip.write(data.content)
	with ZipFile(zipfile, 'r') as zip:
		zip.extract(product_key + '_with_ann.csv', path='media')
		zip.extract(product_key + '_metadata.csv', path='media')
		zip.extract(product_key + '.txt', path='media')

def download_index(session):
	# select data by County
	session.post(SITE + '/rest/geoSearch/geoassist',
		data={'log': 't', 'src': 'geoassist', 'param': 'geo', 'ga.summaryLevel': '050',
			'selections':'All Counties within United States and Puerto Rico~County~050~2018'})
	# there's about 40k results. just get them all (the 75-per-page limit is a UI thing only)
	res = session.get(SITE + '/rest/topicsNav/nav?N=0&startIndex=0&results=50000&rnd=1560602434760')
	with io.open('census.json', 'wb') as fd:
		fd.write(res.content)

def sample(session, n):
	with io.open('census.json', 'r') as fd:
		records = json.load(fd)['AllRecords']['SearchRecords']['Records']
	total = records['TotalNumRecsAvailable']
	results = records['Results']
	for i in range(n):
		index = random.randrange(total)
		download(session, results[index])

def download_by_id(session, id):
	with io.open('census.json', 'r') as fd:
		results = json.load(fd)['AllRecords']['SearchRecords']['Records']['Results']
	download(session, next(prod for prod in results if prod['p_product_key'] == id))

def main(args):
	session = requests.Session()
	if args[0] == 'index':
		download_index(session)
	elif args[0] == 'download':
		for id in args[1:]:
			download_by_id(session, id)
	elif args[0] == 'random':
		sample(session, int(args[1]))
	else:
		print "index (download census.json; takes ~50s and uses ~24MB)"
		print "random <number of IDs> (random sampling from index)"
		print "download <id...> (download dataset by ID; needs index)"

if __name__ == "__main__":
    status = main(sys.argv[1:])
    sys.exit(status)
