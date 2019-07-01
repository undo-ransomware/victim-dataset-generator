def quota(s):
	office = 8/40.
	s.combine('docx', 'odt')
	s.combine('pptx', 'odp')
	s.combine('xlsx', 'ods')
	s.sample('doc', office, 2/25.)
	s.sample('docx', office, 4/25.)
	s.sample('odt', office, 4/25.)
	s.sample('xls', office, 1/25.)
	s.sample('xlsx', office, 2/25.)
	s.sample('ods', office, 2/25.)
	s.sample('ppt', office, 2/25.)
	s.sample('pptx', office, 4/25.)
	s.sample('odp', office, 4/25.)

	img = 15/40.
	s.filter('png', lambda dbb, count: count if dbb >= 40 else 0)
	s.sample('jpg', img, 5/10.)
	s.sample('png', img, 2/10.)
	s.sample('pdf', img, 3/10.)

	media = 8/40.
	s.sample('m4a', media, 1/25.)
	s.sample('mp3', media, 3/25.)
	s.sample('wav', media, 1/25.)
	s.sample('mp4', media, 15/25.)
	s.sample('mts', media, 5/25.)
	s.sample('zip', media, 7/8.)
	s.sample('rar', media, 1/8.)

	plain = 1/40.
	s.combine('md', 'txt', 'tex')
	s.combine('svg', 'xml')
	s.sample('txt', plain, 1/8.)
	s.sample('md', plain, 1/8.)
	s.sample('tex', plain, 1/8.)
	s.sample('html', plain, 1/8.)
	s.sample('csv', plain, 3/8.)
	s.sample('svg', plain, 1/8.)
