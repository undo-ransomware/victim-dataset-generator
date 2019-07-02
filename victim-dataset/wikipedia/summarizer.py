import requests
from lxml import etree
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

try:
	stopwords.words("english")
except LookupError:
	nltk.download('stopwords')
	nltk.download('punkt')
stop = set(stopwords.words('english'))
nopunct = re.compile('\w')

def tokenize(text):
	return [word for word in nltk.word_tokenize(text.lower()) if word not in stop and nopunct.match(word)]

def extract_keywords(text):
	return dict(Counter([word for para in text for word in tokenize(para)]).most_common(20))

def score(sent, keywords):
	words = tokenize(sent)
	if len(words) == 0:
		return -1
	return sum(keywords[word] for word in words if word in keywords) / (len(words) + 3.0)

def summarize(text, keywords, limit):
	scores = dict()
	sentences = [sent for para in text for sent in nltk.sent_tokenize(para)]
	if len(sentences) == 0:
		return []
	for sent in sentences:
		scores[sent] = score(sent, keywords)
	max_score = max(scores.values())

	important = set()
	for sent in sorted(sentences, key=lambda s: scores[s], reverse=True):
		if scores[sent] < max_score / 2.5:
			break
		important.add(sent)
		if len(important) == 7:
			break
		if len(" ".join(important)) > limit:
			break
	return [sent for sent in sentences if sent in important]

def main(args):
	keywords = extract_keywords(args)
	print "\n".join(summarize(args, keywords, float("inf")))
	return 0

if __name__ == "__main__":
    import sys 
    status = main(sys.argv[1:])
    sys.exit(status)
