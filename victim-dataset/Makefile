TARGETS=uni.pdf fratz.pdf uni.mimetypes.txt fratz.mimetypes.txt

all: $(TARGETS)

clean:
	rm -f $(TARGETS) log10.so

%.pdf: %.psv
	cp $< temp.psv
	sqlite3 -batch :memory: '.read filesizes.sql'
	R --no-save -f filesize.r
	mv temp.pdf $@
	mv temp.unmapped $*.unmapped
	rm temp.psv

%.mimetypes.txt: %.psv log10.so
	cp $< temp.psv
	sqlite3 -batch :memory: '.read mimetypes.sql'
	mv temp.mimetypes.txt $*.mimetypes.txt
	mv temp.storage.txt $*.storage.txt
	rm temp.psv

log10.so: log10.c
	gcc -fPIC -shared $^ -o $@ -lm
