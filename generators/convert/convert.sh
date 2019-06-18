#!/bin/bash
#sudo apt install libreoffice pandoc ffmpeg
rm -rf media
mkdir media converted
ln ../wikipedia/*.{docx,pptx,yaml} ../wikimedia/media/*.{ogg,oga,webm,ogv} ../factfinder/media/*.csv media
for file in media/*.docx; do
	name="${file##*/}"
	name="converted/${name%.docx}"
	pandoc -f docx -t markdown -o "$name.md" "$file"
	pandoc -f docx -t latex -o "$name.tex" "$file"
	pandoc -f docx -t html -o "$name.html" "$file"
	libreoffice --convert-to 'doc:MS Word 97' --outdir converted "$file"
	libreoffice --convert-to odt:writer8 --outdir converted "$file"
	libreoffice --convert-to pdf:writer_pdf_Export --outdir converted "$file"
	libreoffice --convert-to txt:Text --outdir converted "$file"
	libreoffice --convert-to html:writerglobal8_HTML --outdir converted "$file" # FIXME no images
done
for file in media/*.pptx; do
	libreoffice --convert-to 'ppt:MS PowerPoint 97' --outdir converted "$file"
	libreoffice --convert-to odp:impress8 --outdir converted "$file"
done
for file in media/*.csv; do
	libreoffice --convert-to 'xls:MS Excel 97' --outdir converted "$file"
	libreoffice --convert-to 'xlsx:Calc MS Excel 2007 XML' --outdir converted "$file"
	libreoffice --convert-to ods:calc8 --outdir converted "$file"
done
for file in media/*.{ogg,oga}; do
	name="${file##*/}"
	name="converted/${name%.*}"
	ffmpeg -i "$file" -c:a aac -vbr 5 $name.aac
	ffmpeg -i "$file" -c:a mp3 -vbr 5 $name.mp3
done
for file in media/*.{webm,ogv}; do
	ext=${file##*.}
	name="${file##*/}"
	name="converted/${name%.*}"
	[ $ext == webm ] || ffmpeg -i "$file" -c:v libvpx-vp9 -c:a libopus -y $name.webm
	[ $ext == ogv ] || ffmpeg -i "$file" -c:v libtheora -c:a libvorbis -y $name.ogv
	ffmpeg -i "$file" -c:v h264 -c:a aac -y $name.mp4
	ffmpeg -i "$file" -c:v mpeg2video -c:a ac3 -f vob -y $name.mpeg
done
