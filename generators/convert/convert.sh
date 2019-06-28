#!/bin/bash
#sudo apt install libreoffice pandoc ffmpeg

for file in media/*.docx; do
	if [ "$file" != "${file%.small.docx}.small.docx" ]; then
		name="${file##*/}"
		name="converted/${name%.docx}"
		[ -s "$name.md" ] || pandoc -f docx -t markdown -o "$name.md" "$file"
		[ -s "$name.tex" ] || pandoc -f docx -t latex -o "$name.tex" "$file"
		[ -s "$name.doc" ] || libreoffice --convert-to 'doc:MS Word 97' --outdir converted "$file"
		[ -s "$name.odt" ] || libreoffice --convert-to odt:writer8 --outdir converted "$file"
		[ -s "$name.pdf" ] || libreoffice --convert-to pdf:writer_pdf_Export --outdir converted "$file"
		# use libreoffice to convert to .txt because pandoc generates plaintext with markup
		[ -s "$name.txt" ] || libreoffice --convert-to txt:Text --outdir converted "$file"
		# create additional, smaller office files from plaintext files because the originals
		# don't get smaller than ~40k (python-docx's predefined styles). these won't get YAML
		# provenance metadata files, but without images all licensing stuff is in the main file
		# anyway.
		[ -s "${name}.small.docx" ] || libreoffice --convert-to 'small.docx:MS Word 2007 XML' --outdir converted "$name.txt"
		[ -s "${name}.small.doc" ] || libreoffice --convert-to 'small.doc:MS Word 97' --outdir converted "$name.txt"
		[ -s "${name}.small.odt" ] || libreoffice --convert-to small.odt:writer8 --outdir converted "$name.txt"
	fi
done
for file in media/*.pptx; do
	name="${file##*/}"
	name="converted/${name%.*}"
	[ -s "$name.ppt" ] || libreoffice --convert-to 'ppt:MS PowerPoint 97' --outdir converted "$file"
	[ -s "$name.odp" ] || libreoffice --convert-to odp:impress8 --outdir converted "$file"
done
for file in media/*.csv; do
	name="${file##*/}"
	name="converted/${name%.*}"
	[ -s "$name.xls" ] || libreoffice --convert-to 'xls:MS Excel 97' --outdir converted "$file"
	[ -s "$name.xlsx" ] || libreoffice --convert-to 'xlsx:Calc MS Excel 2007 XML' --outdir converted "$file"
	[ -s "$name.ods" ] || libreoffice --convert-to ods:calc8 --outdir converted "$file"
done

pffmpeg() {
	while [ $(pidof ffmpeg | tr ' ' \\n | wc -l) -gt 15 ]; do sleep 1; done
	ffmpeg "$@" &
}

rename s/oga$/ogg/ media/*.oga
for file in media/*.ogg; do
	name="${file##*/}"
	name="converted/${name%.*}"
	[ -s "$name.m4a" ] || pffmpeg -i "$file" -c:a aac "$name.m4a"
	[ -s "$name.mp3" ] || pffmpeg -i "$file" -c:a mp3 "$name.mp3"
	[ -s "$name.wav" ] || pffmpeg -i "$file" -c:a pcm_u8 -ar 4000 -ac 1 "$name.wav"
done
for file in media/*.{webm,ogv}; do
	ext=${file##*.}
	name="${file##*/}"
	name="converted/${name%.*}"
	[ -s "$name.webm" ] || [ $ext == webm ] || pffmpeg -i "$file" -c:v libvpx-vp9 -c:a libopus -y "$name.webm"
	[ -s "$name.ogv" ] || [ $ext == ogv ] || pffmpeg -i "$file" -c:v libtheora -c:a libvorbis -y "$name.ogv"
	[ -s "$name.mp4" ] || pffmpeg -i "$file" -c:v h264 -c:a aac -y "$name.mp4"
	[ -s "$name.mts" ] || pffmpeg -i "$file" -c:v mpeg2video -c:a ac3 -f vob -y "$name.mts"
done
