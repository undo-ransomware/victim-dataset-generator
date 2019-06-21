TARGETS=uni.pdf fratz.pdf uni.mimetypes.txt fratz.mimetypes.txt

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

%.pdf: %.psv
	cp $^ temp.psv
	sqlite3 -batch :memory: '.read filesizes.sql'
	R --no-save -f filesize.r
	mv temp.pdf $@
	mv temp.unmapped $*.unmapped
	rm temp.psv

%.mimetypes.txt: %.psv
	cp $^ temp.psv
	sqlite3 -batch :memory: '.read mimetypes.sql'
	mv temp.mimetypes.txt $@
	rm temp.psv
