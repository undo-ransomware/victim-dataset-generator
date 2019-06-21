.separator |
.import temp.psv files
.import mimetypes.map mmap
.header on

update files set mimetype=(select "to" from mmap where mimetype like replace("from",'$',"to"))
	where exists(select * from mmap where mimetype like replace("from",'$',"to"));

.output temp.mimetypes.txt
select mimetype, sum(count) as count from files group by mimetype order by count desc;
