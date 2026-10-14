#!/usr/bin/env python3
"""Offline, navigation-restricted Chromium preview of the vanilla deck.

Uses Playwright's set_content and in-memory style/script injection. It checks
interactive rendering but cannot test real HTTP routing or URL/history behavior;
run check_deck.py in an unrestricted browser before production delivery.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
from html import escape


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck',type=Path)
    parser.add_argument('--out',type=Path,default=Path('deck-preview'))
    args=parser.parse_args()
    from playwright.sync_api import sync_playwright
    root=args.deck.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    markup=(root/'index.html').read_text(encoding='utf-8')
    styles=(root/'styles.css').read_text(encoding='utf-8')
    script=(root/'deck.js').read_text(encoding='utf-8')
    markup=markup.replace('<link rel="stylesheet" href="./styles.css" />',f'<style>{styles}</style>')
    markup=markup.replace('<script src="./deck.js" type="module"></script>','')
    errors=[];checks=[];screenshots=[]
    def check(name,good): checks.append({'name':name,'passed':bool(good)})
    with sync_playwright() as p:
        binary=shutil.which('chromium') or shutil.which('google-chrome')
        launch={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
        if binary: launch['executable_path']=binary
        browser=p.chromium.launch(**launch)
        try:
            page=browser.new_page(viewport={'width':1440,'height':810},reduced_motion='reduce')
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(markup)
            # No history entries are possible on 'about:blank', but regular app state works.
            page.evaluate('history.pushState=()=>{};history.replaceState=()=>{};')
            page.evaluate(script)
            count=page.evaluate('window.__deckDebug.scenes.length')
            check('deck loads in Chromium',count>=3)
            page.keyboard.press('ArrowRight')
            check('right arrow changes reveal',page.evaluate('window.__deckDebug.state.step')==1)
            page.keyboard.press('ArrowLeft')
            check('left arrow changes reveal',page.evaluate('window.__deckDebug.state.step')==0)
            for n in range(count):
                scene=page.evaluate('''(n)=>{ const s=__deckDebug.scenes[n]; __deckDebug.navigate(n,s.steps.length-1); return s.id;}''',n)
                page.wait_for_timeout(60)
                name=f'slide-{n+1:02d}-{scene}.png'
                page.screenshot(path=str(out/name),animations='disabled')
                screenshots.append(name)
                dimensions=page.locator('#stage').bounding_box()
                check(f'slide {n+1} within viewport',dimensions['x']>=-1 and dimensions['y']>=-1 and dimensions['width']<=1441 and dimensions['height']<=811)
            page.evaluate('window.__deckDebug.navigate(2,3)')
            page.get_by_role('button',name='Inspect output node').click()
            check('node inspector responds',page.locator('#inspect-label').inner_text()=='OUTPUT')
            page.evaluate('window.__deckDebug.navigate(3,2)')
            slider=page.get_by_role('slider',name='Minimum signal strength percentage')
            slider.fill('70')
            check('slider recomputes retained connections',page.locator('#retained-count').inner_text()=='1 / 3' and page.locator('.pathway.filtered').count()==2)
            page.get_by_role('button',name='RESET EXPERIMENT').click()
            check('reset restores connection count',page.locator('#retained-count').inner_text()=='3 / 3')
            slider.focus(); prev=page.evaluate('window.__deckDebug.state.step');page.keyboard.press('ArrowRight')
            check('slider arrows do not advance slide',page.evaluate('window.__deckDebug.state.step')==prev)
            page.get_by_label('Presentation visual theme').select_option('nocturne')
            check('theme control applies design tokens',page.locator('#stage').get_attribute('data-theme')=='nocturne')
            page.set_viewport_size({'width':390,'height':844})
            page.evaluate('window.__deckDebug.navigate(0,0)')
            page.screenshot(path=str(out/'mobile-letterboxed.png'),animations='disabled')
            screenshots.append('mobile-letterboxed.png')
            box=page.locator('#stage').bounding_box()
            check('mobile viewport preserves 16:9 ratio',abs(box['width']/box['height']-16/9)<.001)
            check('no JavaScript exceptions',not errors)
        finally: browser.close()
    try:
        from PIL import Image,ImageDraw
        tiles=[]
        for name in screenshots:
            if name.startswith('mobile-'):continue
            with Image.open(out/name) as image:
                image=image.convert('RGB');image.thumbnail((640,360))
                tile=Image.new('RGB',(660,390),'#ffffff');tile.paste(image,((660-image.width)//2,8));ImageDraw.Draw(tile).text((12,366),name,fill='#19283c');tiles.append(tile)
        if tiles:
            sheet=Image.new('RGB',(1320,((len(tiles)+1)//2)*390),'#e8edf4')
            for i,tile in enumerate(tiles):sheet.paste(tile,((i%2)*660,(i//2)*390))
            sheet.save(out/'contact-sheet.png')
    except ImportError: pass
    report={'checks':checks,'passed':all(x['passed'] for x in checks),'errors':errors,'screenshots':screenshots,'limitation':'No URL history/deep-link tests: in-memory about:blank render. Run check_deck.py on an unrestricted host for those.'}
    (out/'report.json').write_text(json.dumps(report,indent=2))
    for x in checks: print(('PASS' if x['passed'] else 'FAIL'),x['name'])
    print('Result:', 'PASS' if report['passed'] else 'FAIL','— artifacts at',out)
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':main()
