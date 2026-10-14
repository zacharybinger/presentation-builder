#!/usr/bin/env python3
"""In-memory preview when URL navigation is blocked. Does not test history or file opening."""
import argparse
import json
from pathlib import Path
from browser_support import launch_browser, frames, seek, stage_fits, contact_sheet
from export_deck import bundle_html


def main():
    from playwright.sync_api import sync_playwright
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck',type=Path);parser.add_argument('--out',type=Path,default=Path('deck-preview'));parser.add_argument('--browser')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    markup,_=bundle_html(args.deck);errors=[];checks=[];screenshots=[]
    with sync_playwright() as pw:
        engine=launch_browser(pw,args.browser)
        try:
            page=engine.new_page(viewport={'width':1440,'height':810},reduced_motion='reduce')
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.route('**/*',lambda r:(errors.append('Unbundled resource: '+r.request.url),r.abort()))
            page.evaluate('history.pushState=()=>{};history.replaceState=()=>{};')
            page.set_content(markup,wait_until='load')
            for row in frames(page):
                seek(page,row['index'],row['steps']-1)
                name=f'slide-{row["index"]+1:02d}.png';page.screenshot(path=str(args.out/name),animations='disabled');screenshots.append(name)
                detail=stage_fits(page);checks.append({'scene':row['index'],'passed':detail['ok'],'detail':detail})
        finally:engine.close()
    report={'passed':not errors and all(c['passed'] for c in checks),'checks':checks,'errors':errors,'not_tested':['Keyboard, widgets, deep links, browser history, native file opening']}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');contact_sheet(args.out,screenshots)
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
