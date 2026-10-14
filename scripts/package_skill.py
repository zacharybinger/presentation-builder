#!/usr/bin/env python3
"""Build a portable skill ZIP from an explicit file list, excluding local research."""
import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
from validate_skill import ROOT,validate


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    errors,files=validate()
    if errors:raise SystemExit('\n'.join(errors))
    if args.out.resolve() in {p.resolve() for p in files}:raise SystemExit('Output cannot overwrite a package source')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(args.out,'w',ZIP_DEFLATED) as archive:
        for p in files:
            info=ZipInfo('presentation-builder/'+p.relative_to(ROOT).as_posix(),date_time=(2026,10,13,0,0,0))
            info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16
            archive.writestr(info,p.read_bytes())
    print(f'Packaged {len(files)} files: {args.out.resolve()} ({args.out.stat().st_size:,} bytes)')

if __name__=='__main__':main()
