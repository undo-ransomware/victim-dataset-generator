#!/bin/bash
download() {
	echo "$@"
	python wikipedia.py "$@"
	python wikipedia2office.py "$@"
	sleep 10
}

for title in "$@"; do
	download "$title"
	python links.py "$title" | while read page; do
		download "$page"
	done
done
