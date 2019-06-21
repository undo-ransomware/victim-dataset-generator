library(RColorBrewer)

files=read.table('temp.psv',sep='|',header=T)
labels=c(round(10^(0:29/10)),
	paste(round(10^(0:9/10), 1), 'k', sep=''),
	paste(round(10^(10:29/10)), 'k', sep=''),
	paste(round(10^(0:9/10), 1), 'M', sep=''),
	paste(round(10^(10:29/10)), 'M', sep=''),
	paste(round(10^(0:9/10), 1), 'G', sep=''),
	paste(round(10^(10:19/10)), 'G', sep=''))
maxk=round(max(files$count)/1000)

pdf('temp.pdf', 20, 14)
#plot(c(0,105), c(0, 1000*maxk), type='n', axes=F, xlab='filesize', ylab='count')
# usable range: 100 bytes to 100MB
plot(c(20,80), c(0, 1000*maxk), type='n', axes=F, xlab='filesize', ylab='count')

axis(1, 0:109, labels=labels, las=3)
abline(v=10*log10(10^(0:10)), col='#cccccc')
temp=merge(2:9, 10^(0:10), by=NULL)
abline(v=10*log10(temp$x*temp$y), lty=2, col='#cccccc')

axis(2, at=1000*0:maxk, labels=paste(0:maxk, 'k', sep=''), las=2)
abline(h=1000*0:maxk, col='#cccccc')

# colors=brewer.pal(8,'Set1') but without yellow
colors=c('#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#a65628','#f781bf')
x=0
for (level in levels(files$ext)) {
	segment=files[files$ext==level,]
	col=colors[1 + x %% length(colors)]
	lines(segment$dbb, segment$count, type='l', col=col)
	points(segment$dbb, segment$count, type='p', col=col, pch=floor(x/length(colors)) + 1)
	x=x+1
}
legend(73, 1000 * maxk, levels(files$ext), col=colors[1 + 0:x %% length(colors)], lty=1, pch=floor(0:x/length(colors)) + 1)
