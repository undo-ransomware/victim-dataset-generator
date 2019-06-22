library(RColorBrewer)

files=read.table('temp.psv',sep='|',header=T)
labels=c(round(10^(0:29/10)),
	paste(round(10^(0:9/10), 1), 'k', sep=''),
	paste(round(10^(10:29/10)), 'k', sep=''),
	paste(round(10^(0:9/10), 1), 'M', sep=''),
	paste(round(10^(10:29/10)), 'M', sep=''),
	paste(round(10^(0:9/10), 1), 'G', sep=''),
	paste(round(10^(10:19/10)), 'G', sep=''))
# colors=brewer.pal(8,'Set1') but without yellow
colors=c('#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#a65628','#f781bf')
pdf('temp.pdf', 20, 14)

mkplot = function(levels, title, range=c(20,73)) {
	maxk = 0
	count = 0
	size = 0
	for (level in levels) {
		segment = files[files$ext==level,]
		maxk = max(segment$count, maxk)
		count = count + sum(segment$count)
		size = size + sum(10^(segment$dbb / 10) * segment$count)
	}
	maxk = maxk / 1000
	size = round(size / 1000000)
	#plot(c(0,105), c(0, 1000*maxk), type='n', axes=F, xlab='filesize', ylab='count')
	# usable range: 100 bytes to ~20MB. there's a long tail with a few huge files
	plot(range, c(0, 1000*maxk), type='n', axes=F, xlab='filesize', ylab='count',
		main=paste(title, ' (', count, ' files, ', size, ' MB)', sep=''))

	axis(1, 0:109, labels=labels, las=3)
	abline(v=10*log10(10^(0:10)), col='#cccccc')
	temp=merge(2:9, 10^(0:10), by=NULL)
	abline(v=10*log10(temp$x*temp$y), lty=2, col='#cccccc')

	axis(2, at=1000*0:maxk, labels=paste(0:maxk, 'k', sep=''), las=2)
	abline(h=1000*0:maxk, col='#cccccc')
	abline(h=0:10 * 100, col='#cccccc', lty=2)

	x=0
	for (level in levels) {
		segment=files[files$ext==level,]
		col=colors[1 + x %% length(colors)]
		lines(segment$dbb, segment$count, type='l', col=col)
		nonzero=segment[segment$count > 0,]
		points(nonzero$dbb, nonzero$count, type='p', col=col, pch=floor(x/length(colors)) + 1)
		x=x+1
	}
	legend(range[2] - 3, 1000 * maxk, levels, col=colors[1 + 0:x %% length(colors)], lty=1, pch=floor(0:x/length(colors)) + 1)
}

mkplot(levels(files$ext), 'all files (except prefiltered)')
mkplot(c('doc','docx','odt','rtf','xls','xlsx','ods','csv','ppt','pptx','odp'), '"productivity" (office) files')
mkplot(c('doc','docx','odt','rtf'), '"productivity" (office) files: word processor')
mkplot(c('xls','xlsx','ods'), '"productivity" (office) files: spreadsheets')
mkplot(c('ppt','pptx','odp'), '"productivity" (office) files: presentations', c(43, 90))
mkplot(c('txt','md','tex','csv','xml','html'), 'plaintext office-like formats')
mkplot(c('jpg','png','bmp','pdf','ps','tif'), 'images, PDFs and likely scanned stuff')
mkplot(c('zip','tgz','rar'), 'archives', c(30, 105))
mkplot(c('m4a','mp3','ogg','wav','mp4','mpeg','ogv','webm'), 'media files', c(40, 95))
mkplot(c('html','js','css','gif','php','png','svg'), 'curiosities: saved websites and probable website resources', c(17, 60))
mkplot(c('c','py','java'), 'curiosities: source code')
