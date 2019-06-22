.separator |
.import temp.psv files
.import mimetypes.map mmap
.header on

update files set mimetype=(select "to" from mmap where mimetype like replace("from",'$',"to"))
	where exists(select * from mmap where mimetype like replace("from",'$',"to"));

.output temp.unmapped
select mimetype, sum(count) as count from files
	where not exists(select * from mmap where mimetype = "to") group by mimetype order by count desc;

with recursive cnt(dbb) as (values(0) union all select dbb + 1 from cnt where dbb <= 105),
	types(mimetype, dbb) as (select distinct mimetype, cnt.dbb from files join cnt)
	insert or ignore into files select mimetype, dbb, 0 as count, '' as ext from types;

.output temp.psv
select mmap.ext as ext, cast(dbb as integer) as dbb, sum(count) as count
	from files join mmap on mimetype = "to" where "from" like '%$%' and dbb not in (-1, 1, 2, 4)
	group by mimetype, dbb order by ext asc, dbb asc;
