targets: uni.pdf fratz.pdf

%.pdf: %.psv
	cp $^ temp.psv
	sqlite3 -batch :memory: '.read mimetypes.sql'
	R --no-save -f filesize.r
	mv temp.pdf $@
	rm temp.psv
