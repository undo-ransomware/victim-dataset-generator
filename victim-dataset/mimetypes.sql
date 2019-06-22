.load ./log10.so
.separator |
.import temp.psv files
.import mimetypes.map mmap
.header on

update files set mimetype=(select "to" from mmap where mimetype like replace("from",'$',"to"))
	where exists(select * from mmap where mimetype like replace("from",'$',"to"));

.output temp.mimetypes.txt
select mimetype, sum(count) as num_files, cast(round(sum(count * exp10(dbb / 10.0))) as integer) as num_bytes
	from files where dbb >= 0 group by mimetype order by num_files desc;
.output temp.storage.txt
select mimetype, sum(count) as num_files, cast(round(sum(count * exp10(dbb / 10.0))) as integer) as num_bytes
	from files where dbb >= 0 group by mimetype order by num_bytes desc;
