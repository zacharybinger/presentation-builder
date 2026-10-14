#!/usr/bin/env python3
"""Render every PDF page for visual review, with a contact sheet."""
import argparse
from pathlib import Path
from browser_support import contact_sheet


def main():
    import pymupdf
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True);names=[]
    with pymupdf.open(args.pdf) as document:
        for index,page in enumerate(document):
            name=f'page-{index+1:03d}.png'
            page.get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False).save(args.out/name)
            names.append(name)
    contact_sheet(args.out,names);print(f'Rendered {len(names)} pages to {args.out.resolve()}')

if __name__=='__main__':main()
