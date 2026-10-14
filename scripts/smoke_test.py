#!/usr/bin/env python3
"""Exercise an isolated copy of the installable package, including browser/PDF regressions."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from validate_skill import ROOT,validate


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,help='Keep generated QA artifacts here (must not exist)');args=parser.parse_args()
    errors,files=validate()
    if errors:raise SystemExit('\n'.join(errors))
    temp=None
    if args.out:
        workspace=args.out.resolve();workspace.mkdir(parents=True,exist_ok=False)
    else:
        temp=tempfile.TemporaryDirectory(prefix='presentation-builder-smoke-');workspace=Path(temp.name)
    try:
        installed=workspace/'installed/presentation-builder'
        for p in files:
            dest=installed/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        scripts=installed/'scripts'
        def run(script,*arguments,expect_success=True):
            result=subprocess.run([sys.executable,str(scripts/script),*map(str,arguments)],cwd=workspace,capture_output=True,text=True)
            if (result.returncode==0)!=expect_success:raise RuntimeError(f'{script}: unexpected exit {result.returncode}\n{result.stdout}\n{result.stderr}')
            print('PASS:',script,*arguments,flush=True)
            return result
        run('validate_skill.py')
        run('create_deck.py','--title','Portable smoke deck','--output','deck')
        run('check_deck.py','deck','--out','qa','--interaction-test',scripts/'starter_interactions.py')
        for mode in ['final','all']:
            extra=['--include-reveals'] if mode=='all' else []
            run('export_deck.py','deck','--out',mode,*extra)
            run('verify_exports.py',f'{mode}/presentation.html',f'{mode}/presentation.pdf')
        run('render_pdf.py','final/presentation.pdf','--out','pdf-review')
        run('preview_deck.py','deck','--out','in-memory-preview')
        # One short custom scene catches assumptions about demo slide count, titles, and widgets.
        single=workspace/'single';single.mkdir()
        (single/'index.html').write_text('''<!doctype html><html><head><style>
          html,body{margin:0}#stage{position:absolute;left:0;top:0;width:1600px;height:900px;transform-origin:top left}
          @media print{#stage{transform:none!important}}
          </style></head><body><main id="stage"><h1>Hi</h1><p id="result"></p></main>
          <script>function resize(){document.querySelector('#stage').style.transform=`scale(${Math.min(innerWidth/1600,innerHeight/900)})`}
          addEventListener('resize',resize);resize();
          window.__presentationExport={frames:()=>[{index:0,steps:1,title:'Hi'}],
            goto:async()=>{await new Promise(r=>setTimeout(r,20));document.querySelector('#result').textContent='Ready'},freeze:()=>{}};
          </script></body></html>''')
        run('check_deck.py','single','--out','single-qa')
        run('export_deck.py','single','--out','single-final')
        run('verify_exports.py','single-final/presentation.html','single-final/presentation.pdf')
        # Check a 12-scene deck can use the same controller without overflowing navigation.
        long=workspace/'long';shutil.copytree(workspace/'deck',long)
        js=(long/'deck.js').read_text();js=js.replace('const state =',"scenes.push(...Array.from({length:7},(_,i)=>({...scenes[0],id:'extra-'+i,nav:'Additional scene '+i})));\nconst state =")
        (long/'deck.js').write_text(js)
        run('check_deck.py','long','--out','long-qa')
        # Rendering an unresolved network resource must fail and preserve previous artifacts.
        previous=(workspace/'single-final/presentation.html').read_bytes()
        (single/'index.html').write_text((single/'index.html').read_text().replace("document.querySelector('#result').textContent='Ready'", "await fetch('https://example.invalid/data').catch(()=>{});document.querySelector('#result').textContent='Ready'"))
        run('export_deck.py','single','--out','single-final',expect_success=False)
        assert (workspace/'single-final/presentation.html').read_bytes()==previous
        print(f'PASS: clean-package workflow; artifacts in {workspace}' if args.out else 'PASS: clean-package workflow')
    finally:
        if temp:temp.cleanup()

if __name__=='__main__':main()
