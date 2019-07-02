#!/bin/bash
python random_articles.py $1 | while read page; do
	echo "$page"
	python wikipedia2office.py "$page"
	python wikipedia.py "$page"
	sleep 10
done
