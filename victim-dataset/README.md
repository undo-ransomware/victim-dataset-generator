# general preparation

- install pip requirements: `pip install -r requirements.txt` in a virtualenv
- install the converters: `sudo apt install libreoffice pandoc ffmpeg zip rar`

# Wikimedia Commons: `commons`

- symlink `media` to target directory
- good sources by filetype:
	- `jpeg`: `randomcat 'CC-Zero'` yields ~80% JPEGs
	- `png`: the "PNG that should use vector graphics" category is useful
		- `randomsearch 'deepcat:"PNG that should use vector graphics" deepcat:CC-Zero'`
		- `randomsearch 'deepcat:"PNG that should use vector graphics" deepcat:"PD ineligible"'`
		- `file 'Umbria da The Historical Atlas, by William R. Shepherd, 1911.png'` manually selected to fill the 6.3MB bin
	- `svg`: `randomcat 'PD OpenClipart'` has ~95% yield
	- `ogg`: `search 'deepcat:CC-Zero deepcat:"Ogg files of music by composer"'` (yes, the complete thing!)
	- `ogv` and `webm`: `randomsearch 'deepcat:"Films from the United States government" deepcat:"PD NASA"'` has reasonable filesizes

# United States Census Bureau, American FactFinder: `factfinder`

- symlink `media` to target directory
- download index before use: `python factfinder.py index`
- `csv`: use `python factfinder.py random` to download a random selection of the ~40k datasets

# Wikipedia articles: `wikipedia`

- symlink `media` to target directory
- make sure the license is still BY-CC-SA 3.0; this is currently hardcoded
- use `download_recursive.sh` to download particular articles
	- eg. `NASA Bernie_Sanders Donald_Trump`
	- pages related to the US government tend to have lots of PD images, and long text
- use `download_random.sh` to download random articles
	- this gives lots of stubs, ie. short text
- generated outputs:
	- `html`: raw HTML page, without images but with licensing info included
	- `pptx`: text auto-summarized, with images (emulating some students annoyingly well)
	- `docx`: same as `pptx` but with full text as well

# ZIP and RAR files: `zip`

- symlink `media` to source / target directory for convenience (or just pass the full path)
- use `estimate_bins.py <format>` (in sampler) to find which bins are actually needed
- use `mkzip.py` to directly generate the required bins
	- `python mkzip.py zip media test bins...` when testing
	- `python mkzip.py zip media media bins...` is safe to use and good for generating the dataset
- run it in a loop (`for x in 1 2 3 4 5; do python mkzip.py zip media media bins...; done`) because it doesn't always exactly hit the target size

# generic File Format Conversion: `convert`

- symlink `media` to source directory
- symlink `converted` to target directory
	- local directory for testing
	- same as source directory when actually generating dataset
- uses pandoc, libreoffice and ffmpeg, so make sure they're installed
	- `ffmpeg -codecs` lists supported audio/video codecs
	- run the macro in `FilterList.fodt` to find LibreOffice's exporters
	- pandoc formats documented in its manpage
- ffmpeg codecs matter a lot for a file's entropy distribution, much more than the container format
- pandoc / LibreOffice conversions for text:
	- `docx` → `md` using pandoc (Markdown)
	- `docx` → `tex` using pandoc (LaTeX)
	- `docx` → `doc` using LibreOffice (MS Word Legacy)
	- `docx` → `odt` using LibreOffice (OpenDocument Text)
	- `docx` → `pdf` using LibreOffice
	- `docx` → `txt` using LibreOffice because pandoc's 'plain' text has quite some markup (eg. `_underlined_`)
	- `txt` → `small.docx`, `small.doc`, `small.odt` using LibreOffice to get small office files (which are common)
- other LibreOffice conversions:
	- `pptx` → `ppt` (MS Powerpoint Legacy)
	- `pptx` → `odp` (OpenDocument Presentation)
	- `csv` → `xsl` (MS Excel Legacy)
	- `csv` → `xslx` (MS Excel Modern)
	- `csv` → `ods` (OpenDocument Spreadsheet)
- ffmpeg conversions:
	- `ogg` → `m4a` using AAC codec (guessed codec but it's the standard-suggested one)
	- `ogg` → `mp3`
	- `ogg` → `wav` as 4kHz 8-bit mono PCM (for reasonable filesizes)
	- `ogv` and `webm` are converted to each other because input files are split ~50/50
	- `ogv` → `webm` as VP9 / OPUS as standardized
	- `webm` → `ogv` as Theora / Vorbis (obviously)
	- `ogv` / `webm` → `mp4` using H.264 / AAC (this is what modern smartphones record)
	- `ogv` / `webm` → `mts`
		- using an MPEG transport stream because that's what the stats suggest
		- guessing for DVD codecs, ie. MPEG-2 + AC3 (likely)
