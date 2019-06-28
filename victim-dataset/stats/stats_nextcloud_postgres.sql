select oc_mimetypes.mimetype, case size when 0 then -1 else round(10*log(size)) end as dbb, count(*) as count,
case when position('.' in name) = 0 then '' when position('.' in reverse(name)) > 5 then '...' else lower(reverse(split_part(reverse(name), '.', 1))) end as ext
from oc_filecache join oc_mimetypes on oc_mimetypes.id = oc_filecache.mimetype where path like 'files/%' and mimepart <> 1
group by oc_mimetypes.mimetype, ext, dbb order by oc_mimetypes.mimetype asc, ext asc, dbb desc;
