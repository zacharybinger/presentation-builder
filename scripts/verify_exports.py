#!/usr/bin/env python3
"""Verify standalone file:// HTML offline, all reveals, and PDF geometry/page count."""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from browser_support import launch_browser, frames, seek, stage_fits
from export_deck import validate_offline_markup


def run(html_file,pdf_file,browser=None,in_memory=False,include_reveals=None):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader
    html_file=Path(html_file).resolve();source=html_file.read_text(encoding='utf8')
    pdf=PdfReader(str(pdf_file));checks=[];errors=[];external=[]
    def note(name,result,detail=None):checks.append({'check':name,'pass':bool(result),'detail':detail})
    validate_offline_markup(source)
    note('PDF has pages',len(pdf.pages)>0)
    for i,page in enumerate(pdf.pages):
        w=float(page.mediabox.width);h=float(page.mediabox.height)
        note(f'PDF page {i+1} is 16:9',h>0 and abs(w/h-16/9)<.003)
    note('PDF retains selectable text',any((p.extract_text() or '').strip() for p in pdf.pages))
    class Metadata(HTMLParser):
        mode='final'
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if tag=='meta' and a.get('name')=='presentation-pdf-mode':self.mode=a.get('content')
    meta=Metadata();meta.feed(source)
    all_reveals=meta.mode=='all' if include_reveals is None else include_reveals
    with sync_playwright() as pw:
        engine=launch_browser(pw,browser)
        try:
            context=engine.new_context(viewport={'width':1600,'height':900},reduced_motion='reduce',service_workers='block')
            # Only the entry document is permitted. Every external or sibling asset fails.
            def route(request):
                if request.request.is_navigation_request() and request.request.url.split('?',1)[0]==html_file.as_uri():request.continue_()
                else:external.append(request.request.url);request.abort()
            context.route('**/*',route)
            context.set_offline(True)
            page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            if in_memory:
                page.add_init_script('history.pushState=()=>{};history.replaceState=()=>{};')
                page.evaluate('history.pushState=()=>{};history.replaceState=()=>{};')
                page.set_content(source,wait_until='load')
            else:page.goto(html_file.as_uri(),wait_until='load')
            rows=frames(page)
            for item in rows:
                for step in range(item['steps']):
                    seek(page,item['index'],step)
                    detail=stage_fits(page)
                    note(f'Scene {item["index"]+1} reveal {step+1} fits',detail['ok'],detail)
                    broken=page.evaluate('[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.alt||i.src.slice(0,100))')
                    note(f'Scene {item["index"]+1} reveal {step+1} images load',not broken,broken)
            if page.evaluate('Boolean(window.__deckDebug)'):
                seek(page,0,0)
                states=[(r['index'],s) for r in rows for s in range(r['steps'])]
                if len(states)>1:
                    page.keyboard.press('ArrowRight')
                    note('Standalone keyboard advances',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==list(states[1]))
                if not in_memory:
                    last=rows[-1]
                    page.goto(html_file.as_uri()+f'?slide={len(rows)}&step={last["steps"]}',wait_until='load');frames(page)
                    note('Standalone deep link restores state',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==[len(rows)-1,last['steps']-1])
            page.set_viewport_size({'width':390,'height':844})
            for item in rows:
                seek(page,item['index'],item['steps']-1)
                detail=stage_fits(page);note(f'Mobile scene {item["index"]+1} fits',detail['ok'],detail)
            note('No browser script exceptions',not errors,errors)
            note('No external or sibling resources requested',not external,external[:12])
            expected=sum(r['steps'] for r in rows) if all_reveals else len(rows)
            note('PDF page count matches export mode',len(pdf.pages)==expected,{'actual':len(pdf.pages),'expected':expected,'mode':'all' if all_reveals else 'final'})
        finally:engine.close()
    return {'passed':all(c['pass'] for c in checks),'checks':checks,
            'note':'In-memory fallback: file opening/history not tested.' if in_memory else 'Standalone file:// tested offline. Custom widgets and visual quality require separate review.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html',type=Path);parser.add_argument('pdf',type=Path)
    parser.add_argument('--browser');parser.add_argument('--in-memory',action='store_true')
    parser.add_argument('--include-reveals',action='store_true',default=None,help='For older exports without PDF mode metadata')
    args=parser.parse_args()
    try:
        report=run(args.html,args.pdf,args.browser,args.in_memory,args.include_reveals)
        print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
    except Exception as exc:
        print(f'Verification could not complete: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
