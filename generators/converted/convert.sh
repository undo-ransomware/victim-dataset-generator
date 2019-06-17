#!/bin/sh
#sudo apt install libreoffice
for file in media/*.docx; do
	name="${file##*/}"
	name="${name%.docx}"
	pandoc -f docx -t markdown -o "converted/$name.md" "$file"
	pandoc -f docx -t latex -o "converted/$name.tex" "$file"
	libreoffice --convert-to 'doc:MS Word 97' --outdir converted "$file"
	libreoffice --convert-to odt:writer8 --outdir converted "$file"
	libreoffice --convert-to pdf:writer_pdf_Export --outdir converted "$file"
	libreoffice --convert-to txt:Text --outdir converted "$file"
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
