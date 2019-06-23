TARGETS=$(foreach inst,uni fratz,$(inst).pdf $(inst).summary.psv $(inst).mimetypes.txt $(inst).storage.txt)

all: $(TARGETS)

clean:
	rm -f $(TARGETS) log10.so

%.summary.psv: %.psv filesizes.sql
	cp $< temp.psv
	sqlite3 -batch :memory: '.read filesizes.sql'
	mv temp.psv $*.summary.psv
	mv temp.unmapped $*.unmapped

%.pdf: %.summary.psv filesize.r
	cp $< temp.psv
	R --no-save -f filesize.r
	mv temp.pdf $@
	rm temp.psv

%.mimetypes.txt %.storage.txt: %.psv mimetypes.sql log10.so
	cp $< temp.psv
	sqlite3 -batch :memory: '.read mimetypes.sql'
	mv temp.mimetypes.txt $*.mimetypes.txt
	mv temp.storage.txt $*.storage.txt
	rm temp.psv

log10.so: log10.c
	gcc -fPIC -shared $^ -o $@ -lm
