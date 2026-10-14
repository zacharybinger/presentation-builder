#!/usr/bin/env python3
"""Validate the portable skill package without external dependencies or research clones."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parent.parent
TOP_FILES=['SKILL.md','README.md','LICENSE','THIRD_PARTY_NOTICES.md']
DIRECTORIES=['agents','references','scripts','templates','examples']


def package_files(root=ROOT):
    files=[root/name for name in TOP_FILES]
    for directory in DIRECTORIES:
        files.extend(p for p in (root/directory).rglob('*') if p.is_file()
                     and not any(part.startswith('.') or part=='__pycache__' for part in p.relative_to(root).parts)
                     and p.suffix not in ('.pyc','.pyo'))
    return sorted(files)


def validate(root=ROOT):
    errors=[];paths=package_files(root)
    for p in paths:
        if not p.is_file():errors.append(f'Missing required file: {p.relative_to(root)}')
        if p.is_symlink():errors.append(f'Package must not contain symlinks: {p.relative_to(root)}')
    skill=(root/'SKILL.md').read_text()
    front=re.match(r'^---\n(.*?)\n---\n',skill,re.S)
    if not front:errors.append('Missing YAML frontmatter')
    else:
        if not re.search(r'^name: presentation-builder$',front[1],re.M):errors.append('Unexpected skill name')
        if not re.search(r'^description: .{20,}$',front[1],re.M):errors.append('Missing description')
        if not re.search(r'^  version: "\d+\.\d+\.\d+"$',front[1],re.M):errors.append('Version must use major.minor.patch')
    entrypoints=[p for p in paths if p.name=='SKILL.md']
    if entrypoints!=[root/'SKILL.md']:errors.append('Package must expose exactly one SKILL.md')
    allowed={p.resolve() for p in paths}
    for p in paths:
        if p.suffix=='.py':
            try:compile(p.read_text(),str(p),'exec')
            except SyntaxError as exc:errors.append(f'{p.name}: {exc}')
        if p.suffix!='.md':continue
        # Ignore code examples; validate real Markdown navigation links.
        content=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',content):
            target=target.strip('<>').split('#',1)[0]
            if not target or re.match(r'^[a-zA-Z][\w+.-]*:',target):continue
            destination=(p.parent/unquote(target)).resolve()
            if destination not in allowed and not (destination.is_dir() and any(x.is_relative_to(destination) for x in allowed)):
                errors.append(f'Broken/unpackaged link in {p.relative_to(root)}: {target}')
    manifest=json.loads((root/'references/upstream/manifest.json').read_text())
    vendored=set()
    for item in manifest['files']:
        if not re.fullmatch('[0-9a-f]{40}',item['revision']):errors.append(f'Unpinned source: {item["path"]}')
        for key,hashkey in [('path','sha256'),('license_path','license_sha256')]:
            p=root/item[key];vendored.add(p.resolve())
            if p.resolve() not in allowed:errors.append(f'Unpackaged manifest path: {item[key]}');continue
            if hashlib.sha256(p.read_bytes()).hexdigest()!=item[hashkey]:errors.append(f'Hash mismatch: {item[key]}')
    for p in (root/'references/upstream').rglob('*'):
        if p.is_file() and p.name!='manifest.json' and p.resolve() not in vendored:errors.append(f'Unattributed upstream file: {p.relative_to(root)}')
    return errors,paths


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path,nargs='?',default=ROOT);args=parser.parse_args()
    errors,paths=validate(args.root.resolve())
    for e in errors:print('FAIL:',e)
    print(f'{"FAIL" if errors else "PASS"}: {len(paths)} package files, {sum(p.stat().st_size for p in paths if p.exists()):,} bytes')
    return bool(errors)

if __name__=='__main__':sys.exit(main())
