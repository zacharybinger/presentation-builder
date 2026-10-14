#!/usr/bin/env python3
"""Browser QA for any deck implementing the export contract; optional widget assertions."""
from __future__ import annotations
import argparse
import http.server
import importlib.util
import json
from pathlib import Path
import threading
from browser_support import launch_browser, frames, seek, stage_fits, content_overflow, contact_sheet


def make_server(root):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server


def check_deck(root,out,executable=None,interaction_test=None):
    from playwright.sync_api import sync_playwright
    if not (root/'index.html').is_file():raise ValueError('Missing index.html')
    out.mkdir(parents=True,exist_ok=True)
    report={'checks':[],'errors':[],'screenshots':[],'not_tested':[]}
    def check(name,result,detail=''):
        report['checks'].append({'name':name,'passed':bool(result),'detail':detail})
    server=make_server(root)
    url=f'http://127.0.0.1:{server.server_address[1]}/'
    try:
        with sync_playwright() as pw:
            browser=launch_browser(pw,executable)
            try:
                page=browser.new_page(viewport={'width':1440,'height':810},reduced_motion='reduce')
                page.on('pageerror',lambda e:report['errors'].append(str(e)))
                page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
                page.goto(url,wait_until='load')
                rows=frames(page)
                check('Deck initializes',True,f'{len(rows)} scenes')
                starter=page.evaluate('Boolean(window.__deckDebug)')
                if starter:
                    # Flatten actual reveal states instead of assuming five demo slides.
                    states=[(r['index'],step) for r in rows for step in range(r['steps'])]
                    page.goto(url+'?slide=1&step=1',wait_until='load');frames(page)
                    if len(states)>1:
                        page.keyboard.press('ArrowRight')
                        expected=states[1]
                        check('Keyboard advances',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==list(expected))
                        page.go_back(wait_until='load')
                        check('Browser back restores state',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==[0,0])
                        page.go_forward(wait_until='load')
                        check('Browser forward restores state',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==list(expected))
                        page.keyboard.press('ArrowLeft')
                        check('Keyboard reverses',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==[0,0])
                    final=rows[-1]
                    page.goto(url+f'?slide={len(rows)}&step={final["steps"]}&theme=explainer',wait_until='load');frames(page)
                    check('Deep link restores final scene/reveal',page.evaluate('[__deckDebug.state.slide,__deckDebug.state.step]')==[len(rows)-1,final['steps']-1])
                    check('Deep link restores theme',page.locator('#stage').get_attribute('data-theme')=='explainer')
                    page.goto(url,wait_until='load');frames(page)
                else:
                    report['not_tested'].append('Custom controller keyboard/history: add assertions via --interaction-test')
                for row in rows:
                    for step in range(row['steps']):
                        seek(page,row['index'],step)
                        detail=stage_fits(page)
                        check(f'Scene {row["index"]+1}, reveal {step+1}: stage fits',detail['ok'],detail)
                        overflow=content_overflow(page)
                        check(f'Scene {row["index"]+1}, reveal {step+1}: text/control bounds',not overflow,overflow)
                    name=f'slide-{row["index"]+1:02d}.png'
                    page.screenshot(path=str(out/name),animations='disabled')
                    report['screenshots'].append(name)
                if interaction_test:
                    spec=importlib.util.spec_from_file_location('deck_interactions',interaction_test)
                    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                    module.exercise(page,check)
                else:
                    report['not_tested'].append('Deck-specific widgets: exercise manually or use --interaction-test')
                for width,height,label in [(1280,720,'small'),(1920,1080,'large'),(390,844,'mobile')]:
                    page.set_viewport_size({'width':width,'height':height})
                    for row in rows:
                        seek(page,row['index'],row['steps']-1)
                        detail=stage_fits(page)
                        check(f'{label} scene {row["index"]+1} fits',detail['ok'],detail)
                    seek(page,0,rows[0]['steps']-1)
                    name=f'{label}-opening.png';page.screenshot(path=str(out/name),animations='disabled')
                    report['screenshots'].append(name)
                check('No browser errors',not report['errors'],report['errors'])
            finally:browser.close()
    except Exception as exc:
        check('QA completed',False,str(exc))
    finally:
        server.shutdown();server.server_close()
    report['passed']=bool(report['checks']) and all(c['passed'] for c in report['checks'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    contact_sheet(out,report['screenshots'])
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck',type=Path)
    parser.add_argument('--out',type=Path,default=Path('deck-qa'))
    parser.add_argument('--browser')
    parser.add_argument('--interaction-test',type=Path,help='Trusted Python file exporting exercise(page, check)')
    args=parser.parse_args()
    report=check_deck(args.deck.resolve(),args.out.resolve(),args.browser,args.interaction_test)
    failures=[c for c in report['checks'] if not c['passed']]
    print(json.dumps({'passed':report['passed'],'checks':len(report['checks']),'failures':failures,'not_tested':report['not_tested'],'report':str(args.out/'report.json')},indent=2))
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
