TARGETS=uni.pdf fratz.pdf

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

%.pdf: %.psv
	cp $^ temp.psv
	sqlite3 -batch :memory: '.read mimetypes.sql'
	R --no-save -f filesize.r
	mv temp.pdf $@
	rm temp.psv
