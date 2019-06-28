.import uni.psv files
.import mimetypes.map mmap
.header off
.output mime_map.py
select 'mimetypes = {';
select distinct '	''' || ext || ''': ''' || mimetype || ''',' from files join mmap using(ext) order by ext asc;
select '}';
