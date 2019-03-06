#!/usr/bin/env python3
import sys
from pathlib import Path
from zipfile import ZipFile

src_dir, dest_dir = map(Path, sys.argv[1:])
for filename in src_dir.glob('*.*'):
    with ZipFile(str(dest_dir / (filename.stem + '.zip')), 'w') as archive:
        archive.write(str(filename), arcname=filename.name)