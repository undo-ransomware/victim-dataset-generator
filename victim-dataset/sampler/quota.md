# file type classes

- ransomware loves office files, so we overrepresent those
- most of the data (480k files, 568GB) are unidenfitied stuff we cannot possibly create

| class           | size   | parts (1 part = 54GB)                  |
|-----------------|--------|----------------------------------------|
| media files     | 410GB  | 8 parts                                |
| archives        | 430GB  | 8 parts                                |
| images & PDFs   | 828GB  | 15 parts                               |
| plaintext files | 54GB   | 1 part (defined by this filetype)      |
| office files    | 125GB  | 8 parts (deliberately overrepresented) |
| total           | 2403GB | 40 parts                               |

# office files

- omitting `csv` here, it's a plaintext format and accounted for there
- we like open stuff. use as much `od?` as Microsoft's `???x` formats. they're both ZIP files anyway
- dropping `rtf` because it's plaintext, deprecated, somewhat badly specified, and looks like LaTeX anyway
- by file type:
	- 2 parts word processor
	- 2 parts presentation (underrepresented, mostly because we'll otherwise run out of large ones)
	- 1 part spreadsheet (overrepresented, but business critical in some badly-run companies)
- by application:
	- 2 parts Microsoft XML
	- 2 parts OpenOffice / LibreOffice XML (as per "open stuff" above)
	- 1 part Microsoft legacy
- combine OpenDocument and Microsoft XML, then draw from combined frequencies

| type  | files | size   | parts    |
|-------|-------|--------|----------|
| doc   | 20k   |  5.5GB | 2 parts  |
| docx  | 42k   | 20.7GB | 4 parts  |
| odt   | 10k   |  1.8GB | 4 parts  |
| rtf   | 14k   |  1.2GB | —        |
| xls   | 6k    |  1.7GB | 1 part   |
| xlsx  | 13k   |  3.6GB | 2 parts  |
| ods   | 1k    |  ~50MB | 2 parts  |
| csv   | 40k   | 20.6GB | —        |
| ppt   | 3k    |  7.9GB | 2 parts  |
| pptx  | 8k    | 60.2GB | 4 parts  |
| odp   | ~500  |  1.9GB | 4 parts  |
| total | 158k  |  125GB | 25 parts |

# images & PDFs

- `ps`, `bmp` are basically irrelevant (very few files)
- TIFF probably comes almost entirely from scans
	- almost impossible to create the way printer-scanners create them
	- entropy-wise, these should look mostly like either PNG or JPEG
- slightly overrepresenting JPEG because it's much more common in private clouds
- remove small (<10k) PNGs
	- they otherwise dominate the category
	- they're almost certainly website assets for saved websites

| type  | files | size  | parts                              |
|-------|-------|-------|------------------------------------|
| jpg   | 240k  | 403GB | 5 parts (slightly overrepresented) |
| png   | 140k  | 205GB | 2 parts                            |
| pdf   | 217k  | 308GB | 3 parts                            |
| tif   | 16k   |  82GB | —                                  |
| total | 158k  | 998GB | 10 parts                           |

# media files

- number of files is 50/50 audio to video
- size is ~1:4 audio to video
- not preferring open formats because usuers usually cannot choose the format here
- `wav` is surprisingly popular (might be research data, 200k - 2M are very short files)

| type  | files | size   | parts    |
|-------|-------|--------|----------|
| m4a   | 2.0k  |  12GB  | 1 part   |
| mp3   | 7.9k  |  44GB  | 3 parts  |
| ogg   | 0.3k  |   1GB  | —        |
| wav   | 5.5k  |  21GB  | 1 part   |
| mp4   | 3.8k  | 255GB  | 15 parts |
| mts   | 0.6k  |  76GB  | 5 parts  |
| ogv   | 2 (!) | 1GB(!) | —        |
| webm  | 10(!) | 400MB  | —        |
| total | 19.5k | 410GB  | 25 parts |

# archives

- `rar` included mostly because we know it's high-entropy and prone to false alarms
- `tgz` and `*.gz` suggests somewhat atypical use by IT department

| type       | files | size  | parts   |
|------------|-------|-------|---------|
| zip        | 7.2k  | 324GB | 7 parts |
| rar        | 0.3k  |  46GB | 1 parts |
| tgz and gz | 52.0k |  60GB | —       |
| total      | 158k  | 430GB | 8 parts |

# plaintext files

- distribution probably doesn't matter; these stick out as uncompressed anyway
- given how small these are, we WILL run out of them, so the more formats the better
	- HTML is probably saved websites, so not that important
	- using 1 part `tex` because it's similar to `rtf`
	- using 1 part `md` because of NextCloud editor integration
	- combine statistics for `md`, `txt` and `tex`, then draw from combined frequencies
- we have plenty `csv` but that has significantly different entropy (numbers)
- using SVG for XML, hoping it is somewhat representative

| type  | files | size   | parts        |
|-------|-------|--------|--------------|
| txt   | 81k   | 19.7GB | 1 part       |
| md    | 11k   |   52MB | 1 part       |
| tex   | 16k   |  0.2GB | 1 part       | 
| html  | 30k   |  4.5GB | 1 part       |
| csv   | 40k   | 20.6GB | 3 parts      |
| xml   | 14k   |  9.0GB | 1 part (SVG) |
| total | 191k  | 54.1GB | 8 parts      |
