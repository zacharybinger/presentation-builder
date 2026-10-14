#!/usr/bin/env python3
"""Real-browser QA and screenshot runner for the bundled interactive deck.

This checker targets the bundled starter's DOM/test contract. Adapt selectors
when replacing the presentation engine with a React implementation.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import http.server
import json
import os
from pathlib import Path
import shutil
import socketserver
import threading
from urllib.parse import urlencode


def make_server(root: Path):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)
        def log_message(self, *args):
            pass
    class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
        allow_reuse_address = True
    server = Server(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def check_deck(root: Path, out: Path, executable: str | None = None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError('Requires Python Playwright: python -m pip install playwright && python -m playwright install chromium') from e
    out.mkdir(parents=True, exist_ok=True)
    if not (root / 'index.html').is_file() or not (root / 'deck.js').is_file():
        raise RuntimeError('Starter-compatible deck expected: index.html and deck.js')
    server = make_server(root)
    url = f'http://127.0.0.1:{server.server_address[1]}/'
    report = {'url':url,'checks':[],'errors':[],'screenshots':[]}
    def ok(name, result, detail=''):
        report['checks'].append({'name':name,'passed':bool(result),'detail':str(detail)})
    try:
        with sync_playwright() as p:
            chrome_args = {'headless':True, 'args':['--no-sandbox', '--disable-dev-shm-usage']}
            if executable:
                chrome_args['executable_path'] = executable
            elif shutil.which('chromium') or shutil.which('google-chrome'):
                chrome_args['executable_path'] = shutil.which('chromium') or shutil.which('google-chrome')
            browser = p.chromium.launch(**chrome_args)
            try:
                page = browser.new_page(viewport={'width':1440,'height':810},device_scale_factor=1, reduced_motion='reduce')
                page.on('pageerror', lambda e: report['errors'].append(str(e)))
                page.goto(url, wait_until='load')
                page.get_by_role('heading', level=1).wait_for()
                total = page.evaluate('window.__deckDebug?.scenes.length')
                ok('Deck initializes', isinstance(total, int) and total >= 3, f'{total} slides')
                ok('Opening URL points to slide 1', 'slide=1' in page.url, page.url)
                page.screenshot(path=str(out/'slide-01-opening.png'), animations='disabled')
                report['screenshots'].append('slide-01-opening.png')
                page.keyboard.press('ArrowRight')
                ok('Keyboard advances within slide', page.evaluate('window.__deckDebug.state.step') == 1)
                page.keyboard.press('ArrowLeft')
                ok('Keyboard reverses reveal', page.evaluate('window.__deckDebug.state.step') == 0)
                page.go_back(wait_until='load')
                ok('Browser back restores URL state',page.evaluate('window.__deckDebug.state.step') == 1)
                page.go_forward(wait_until='load')
                ok('Browser forward restores URL state',page.evaluate('window.__deckDebug.state.step') == 0)
                for index in range(total):
                    result = page.evaluate('''(index) => {
                      const s = window.__deckDebug.scenes[index];
                      window.__deckDebug.navigate(index, s.steps.length-1);
                      return {id:s.id,step:s.steps.length,header:document.querySelector('#slide-heading').textContent};
                    }''', index)
                    page.wait_for_timeout(90)
                    name=f'slide-{index+1:02d}-{result["id"]}.png'
                    page.screenshot(path=str(out/name), animations='disabled')
                    report['screenshots'].append(name)
                    box=page.locator('#stage').bounding_box()
                    ok(f'Slide {index+1} stage fits desktop',bool(box) and box['width'] <= 1440.5 and box['height'] <= 810.5 and box['x'] >= -1 and box['y'] >= -1,box)
                    visible=page.locator('#scene-root [data-at]:not([aria-hidden="true"])').count()
                    ok(f'Slide {index+1} final reveals visible', visible > 0 or index == 0, f'{visible} progressive elements')
                page.goto(url + '?slide=3&step=4&theme=explainer', wait_until='load')
                ok('Direct link restores slide and reveal', page.evaluate('window.__deckDebug.state.slide===2 && window.__deckDebug.state.step===3'))
                ok('Direct link restores style',page.locator('#stage').get_attribute('data-theme')=='explainer')
                # An actual diagram selection, not an inert decoration.
                page.get_by_role('button', name='Inspect output node').click()
                ok('Inspectable diagram updates text',page.locator('#inspect-label').inner_text()=='OUTPUT')
                # The live slider changes line visibility AND explanatory output.
                page.goto(url + '?slide=4&step=3&theme=signal', wait_until='load')
                slider=page.get_by_role('slider',name='Minimum signal strength percentage')
                slider.fill('70')
                ok('Slider updates retained path count',page.locator('#retained-count').inner_text()=='1 / 3')
                ok('Slider changes SVG graph',page.locator('.pathway.filtered').count()==2)
                page.get_by_role('button',name='RESET EXPERIMENT').click()
                ok('Reset restores initial values',page.locator('#retained-count').inner_text()=='3 / 3' and page.locator('#threshold-display').inner_text()=='20')
                # Inputs should consume arrow keys, not advance the presentation.
                slider.focus(); initial_step=page.evaluate('window.__deckDebug.state.step')
                page.keyboard.press('ArrowRight')
                ok('Input keyboard does not navigate presentation',page.evaluate('window.__deckDebug.state.step')==initial_step)
                # Portrait/mobile: expected letterbox rather than reflow.
                page.set_viewport_size({'width':390,'height':844})
                page.goto(url + '?slide=1&step=1&theme=nocturne', wait_until='load')
                page.screenshot(path=str(out/'mobile-letterboxed.png'),animations='disabled')
                report['screenshots'].append('mobile-letterboxed.png')
                b=page.locator('#stage').bounding_box()
                ok('Small viewport preserves 16:9 aspect',bool(b) and abs(b['width']/b['height']-16/9)<.002,b)
                ok('Small viewport stage fits',bool(b) and b['width'] <= 390.5 and b['height'] <= 844.5,b)
                ok('No JavaScript page exceptions',len(report['errors'])==0,report['errors'])
            finally:
                browser.close()
    finally:
        server.shutdown(); server.server_close()
    # Make a contact sheet without requiring Pillow for basic checks.
    try:
        from PIL import Image, ImageOps, ImageDraw
        images=[]
        for name in report['screenshots']:
            if name=='mobile-letterboxed.png': continue
            with Image.open(out/name) as f:
                img=f.convert('RGB'); img.thumbnail((640,360));
                tile=Image.new('RGB',(660,400),'#ffffff')
                tile.paste(img,((660-img.width)//2,12))
                ImageDraw.Draw(tile).text((14,378),name,fill='#19283c')
                images.append(tile)
        if images:
            cols=2; rows=(len(images)+1)//2
            sheet=Image.new('RGB',(cols*660,rows*400),'#e9edf1')
            for i,img in enumerate(images):sheet.paste(img,((i%2)*660,(i//2)*400))
            sheet.save(out/'contact-sheet.png')
    except ImportError: pass
    report['passed'] = all(x['passed'] for x in report['checks'])
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck',type=Path,help='Directory containing starter index.html and deck.js')
    parser.add_argument('--out',type=Path,default=Path('deck-qa'))
    parser.add_argument('--browser',help='Optional Chromium executable')
    args=parser.parse_args()
    report=check_deck(args.deck.resolve(),args.out.resolve(),args.browser)
    for c in report['checks']:
        print(f'{"PASS" if c["passed"] else "FAIL"} — {c["name"]}: {c["detail"]}')
    print(f'Artifacts: {args.out.resolve()}')
    print('RESULT:', 'PASS' if report['passed'] else 'FAIL')
    raise SystemExit(0 if report['passed'] else 1)


if __name__=='__main__':main()
