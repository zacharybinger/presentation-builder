#!/usr/bin/env python3
"""Verify the final TWO-file deliverable with a network-blocked browser + PDF structural checks.

Browser content is loaded in-memory because some automation hosts block file/http
URLs. Thus URL history/native file:// opening require separate manual verification.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import sys


def run(html_file, pdf_file, browser=None):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader
    source=Path(html_file).read_text(encoding='utf8')
    pdf=PdfReader(str(pdf_file))
    checks=[];errors=[];external=[]
    def note(msg,condition,detail=None):checks.append({'check':msg,'pass':bool(condition),'detail':detail})
    note('HTML generated',len(source)>2500)
    note('PDF generated',len(pdf.pages)>0)
    note('No external stylesheet or script tags',not re.search(r'<(?:link|script)\b[^>]*(?:href|src)\s*=\s*["\'](?:https?:|//)',source,re.I))
    note('No unresolved CSS or JS tag references',not re.search(r'<(?:link|script)\b[^>]*(?:href|src)\s*=\s*["\']\./',source,re.I))
    for i,page in enumerate(pdf.pages):
        w=float(page.mediabox.width);h=float(page.mediabox.height)
        note(f'PDF page {i+1} 16:9',abs(w/h-16/9)<.003)
        text=page.extract_text() or ''
        note(f'PDF page {i+1} has text',len(text.strip())>80,{'characters':len(text)})
    markup=source.replace('<head>','<head><script>history.pushState=()=>{};history.replaceState=()=>{};</script>',1)
    with sync_playwright() as pw:
        config={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
        binary=browser or shutil.which('chromium') or shutil.which('google-chrome')
        if binary:config['executable_path']=binary
        engine=pw.chromium.launch(**config)
        try:
            page=engine.new_page(viewport={'width':1600,'height':900},reduced_motion='reduce')
            page.route('**/*',lambda route: (external.append(route.request.url),route.abort()))
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(markup,wait_until='load')
            page.wait_for_function('Boolean(window.__presentationExport || window.__deckDebug)',timeout=10000)
            slides=page.evaluate('''() => window.__presentationExport?.frames() || window.__deckDebug.scenes.map((s,i)=>({index:i,steps:s.steps.length,title:s.id}))''')
            note('Slides render in browser',len(slides)>0)
            for item in slides:
                page.evaluate('''({index,step})=>{if(window.__presentationExport)window.__presentationExport.goto(index,step);else window.__deckDebug.navigate(index,step,{fromUrl:true})}''',{'index':item['index'],'step':item['steps']-1})
                heading=page.locator('h1').first.inner_text() if page.locator('h1').count() else ''
                note(f'Scene {item["index"]+1} has visible heading',bool(heading.strip()),heading[:65])
            page.evaluate('''()=>{if(window.__presentationExport)window.__presentationExport.goto(0,0);else window.__deckDebug.navigate(0,0,{fromUrl:true})}''')
            before=page.evaluate('window.__deckDebug?.state?.step')
            if before is not None and slides[0]['steps']>1:
                page.keyboard.press('ArrowRight')
                note('Keyboard advances scene',page.evaluate('window.__deckDebug.state.step')==1)
            note('No browser script exceptions',not errors,errors)
            note('No requested external resources',not external,external[:12])
            page.set_viewport_size({'width':390,'height':844})
            stage=page.locator('#stage')
            if stage.count():
                bbox=stage.bounding_box()
                note('Mobile retains 16:9',bool(bbox) and abs(bbox['width']/bbox['height']-16/9)<.002)
                note('Mobile stage fits viewport',bool(bbox) and bbox['width']<=391 and bbox['height']<=845)
            note('PDF page count matches scene count',len(pdf.pages)==len(slides),{'pdf':len(pdf.pages),'scenes':len(slides)})
        finally:engine.close()
    return {'passed':all(x['pass'] for x in checks),'checks':checks,'note':'Browser tested via in-memory HTML. Native file:// and History API not tested; require an unrestricted local browser.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html',type=Path)
    parser.add_argument('pdf',type=Path)
    parser.add_argument('--browser',help='Path to Chromium executable')
    args=parser.parse_args()
    try:
        r=run(args.html,args.pdf,args.browser)
        print(json.dumps(r,indent=2))
        return 0 if r['passed'] else 1
    except Exception as e:
        print(f'Verification could not complete: {e}',file=sys.stderr)
        return 2
if __name__=='__main__':sys.exit(main())
