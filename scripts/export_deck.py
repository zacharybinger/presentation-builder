#!/usr/bin/env python3
"""Publish a presentation as exactly one offline HTML plus one 16:9 PDF.

Source may remain modular during authoring (index.html, CSS, JS, local assets).
PDF freezes each slide at its final reveal by default, with interactive state intact
in the HTML. Supports a user-supplied window.__presentationExport interface, or
this skill's legacy window.__deckDebug controller. Uses stdlib + Playwright + pypdf.
"""
from __future__ import annotations
import argparse
import base64
import html as htmlmod
import io
import json
import mimetypes
import re
from pathlib import Path
import sys

URL_FUNC = re.compile(r'url\(\s*(["\']?)(.*?)\1\s*\)', flags=re.I|re.S)
CSS_IMPORT = re.compile(r'@import\s+(?:url\(\s*)?["\']([^"\']+)["\']\s*\)?\s*;', re.I)
ATTR = re.compile(r'([:\w-]+)\s*=\s*(["\'])(.*?)\2', re.S)
CSS_LINK = re.compile(r'<link\b[^>]*>',re.I|re.S)
SCRIPT = re.compile(r'<script\b[^>]*>.*?</script\s*>',re.I|re.S)
LOCAL_MEDIA_TAG = re.compile(r'<(?:img|source|video|audio|image|use|input)\b[^>]*>',re.I|re.S)
DYNAMIC_IMPORT = re.compile(r'(?m)^\s*(?:import\s+(?!\()|export\s+.*from\s+)[^;\n]*(?:from\s*)?["\']([^"\']+)["\']')

class BundleError(RuntimeError): pass


def attributes(tag):
    return {m.group(1).lower(): m.group(3) for m in ATTR.finditer(tag)}


def classify(url):
    url=htmlmod.unescape(url.strip())
    if not url or url.startswith('#') or url.startswith('data:') or url.startswith('blob:'): return 'embedded'
    if url.startswith('//') or re.match(r'^(?:https?:|[\w+.-]+:)',url,re.I): return 'remote'
    if url.startswith('/'): return 'root'
    return 'local'


def resolve_file(path, root, base):
    path=path.split('#',1)[0].split('?',1)[0]
    p=(base/path).resolve()
    if not p.is_relative_to(root): raise BundleError('Local resource escapes deck root: '+str(p))
    if not p.is_file(): raise BundleError('Missing local resource: '+str(p))
    return p


def to_data_url(path):
    mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')


def bundle_css(content,root,base,stack=()):
    def do_import(m):
        path=m.group(1); typ=classify(path)
        if typ != 'local': raise BundleError('CSS @import is not offline-local: '+path)
        p=resolve_file(path,root,base)
        if p in stack: raise BundleError('Cyclic CSS imports: '+str(p))
        return bundle_css(p.read_text(encoding='utf8'),root,p.parent,stack+(p,))
    content=CSS_IMPORT.sub(do_import,content)
    # Any more @import is likely layered/media and cannot be safely inlined.
    if re.search(r'@import\b',content,re.I): raise BundleError('Unsupported @import: inline or compile CSS imports first.')
    def url_sub(m):
        url=m.group(2).strip(); typ=classify(url)
        if typ=='embedded':return m.group(0)
        if typ!='local':raise BundleError('CSS external/root URL not portable: '+url)
        return 'url("'+to_data_url(resolve_file(url,root,base))+'")'
    return URL_FUNC.sub(url_sub,content)


def bundle_html(deck_dir):
    root=deck_dir.resolve(); entry=root/'index.html'
    if not entry.is_file():raise BundleError('Missing index.html: '+str(entry))
    source=entry.read_text(encoding='utf8')
    stats={'styles':0,'scripts':0,'media':0,'bytes_assets':0}
    def link_sub(m):
        tag=m.group(0); a=attributes(tag); rel=a.get('rel','').lower().split()
        url=a.get('href','')
        if 'stylesheet' in rel:
            if classify(url)!='local':raise BundleError('Remote stylesheet: '+url)
            p=resolve_file(url,root,root); css=bundle_css(p.read_text(encoding='utf8'),root,p.parent,(p,))
            stats['styles']+=1
            return '<style data-bundled-from="'+htmlmod.escape(url,quote=True)+'">\n'+css+'\n</style>'
        if any(r in rel for r in ('modulepreload','preload','prefetch')):
            # Prefetch is unnecessary once local resources are inlined.
            return ''
        if any(r in rel for r in ('icon','apple-touch-icon')):
            if classify(url)!='local': raise BundleError('Remote icon asset: '+url)
            return tag.replace(url,to_data_url(resolve_file(url,root,root)))
        return tag
    source=CSS_LINK.sub(link_sub,source)
    def script_sub(m):
        tag=m.group(0)
        head=tag[:tag.index('>')+1]; a=attributes(head); url=a.get('src')
        if not url:return tag
        if classify(url)!='local':raise BundleError('Remote JS runtime: '+url)
        p=resolve_file(url,root,root); code=p.read_text(encoding='utf8')
        if DYNAMIC_IMPORT.search(code) or re.search(r'\bimport\s*\(',code):
            raise BundleError('JS has unresolved imports: compile/bundle it (e.g. Vite build) first: '+str(p))
        # Removing src turns an external script into inline content. Preserve type=module.
        head=re.sub(r'\s+src\s*=\s*(["\']).*?\1','',head,flags=re.I|re.S)
        code=code.replace('</script','<\\/script')
        stats['scripts']+=1
        return head+'\n'+code+'\n</script>'
    source=SCRIPT.sub(script_sub,source)
    def media_sub(m):
        tag=m.group(0); a=attributes(tag)
        if 'srcset' in a:raise BundleError('srcset not yet supported; consolidate into src or prebundle the image')
        for field in ('src','poster','href','xlink:href'):
            u=a.get(field)
            if not u:continue
            typ=classify(u)
            if typ=='embedded':continue
            if typ!='local':raise BundleError('Nonportable media URL: '+u)
            p=resolve_file(u,root,root)
            value=to_data_url(p)
            tag=re.sub(r'(?<![\w:-])'+re.escape(field)+r'\s*=\s*(["\'])'+re.escape(u)+r'\1',lambda match:field+'="'+value+'"',tag,count=1,flags=re.I)
            stats['media']+=1;stats['bytes_assets']+=p.stat().st_size
        return tag
    source=LOCAL_MEDIA_TAG.sub(media_sub,source)
    if re.search(r'<(?:script|link)\b[^>]*\b(?:src|href)\s*=\s*["\'](?:https?:|//)',source,re.I):
        raise BundleError('Unbundled external runtime references remain')
    if re.search(r'<script\b[^>]*\bsrc=',source,re.I):raise BundleError('Unresolved JS source')
    if re.search(r'<link\b[^>]*\brel\s*=\s*["\']stylesheet',source,re.I):raise BundleError('Unresolved CSS stylesheet')
    # No script should rely on loading local files at runtime.
    if re.search(r'\bfetch\s*\(\s*["\'](?:\./|\.\./|/)',source):
        raise BundleError('Local fetch() path found. Embed data as JSON in HTML before exporting.')
    source=source.replace('</head>','<meta name="presentation-export" content="single-file-offline">\n</head>',1)
    return source,stats


def write_pdf(bundled, destination, include_reveals=False, theme=None, browser_path=None):
    try:
        from playwright.sync_api import sync_playwright
        from pypdf import PdfReader, PdfWriter
    except ImportError as e:
        raise BundleError('Install PDF export dependencies: python -m pip install playwright pypdf; python -m playwright install chromium') from e
    # Because page.set_content uses about:blank, stub the URL history API only in this
    # sandboxed export tab. The actual standalone HTML keeps browser history intact.
    markup=bundled.replace('<head>','<head><script>history.pushState=()=>{};history.replaceState=()=>{};</script>',1)
    writer=PdfWriter(); frames=[];errors=[]
    with sync_playwright() as p:
        opts={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
        if browser_path:opts['executable_path']=browser_path
        browser=p.chromium.launch(**opts)
        try:
            page=browser.new_page(viewport={'width':1600,'height':900},device_scale_factor=1,reduced_motion='reduce',accept_downloads=False)
            page.on('pageerror',lambda exc:errors.append(str(exc)))
            page.set_content(markup,wait_until='load')
            page.wait_for_function('Boolean(window.__presentationExport || window.__deckDebug)',timeout=10000)
            metadata=page.evaluate('''() => {
              const e=window.__presentationExport;
              if (e) return e.frames();
              return window.__deckDebug.scenes.map((s,i)=>({index:i,steps:s.steps.length,title:s.nav||s.id}));
            }''')
            if not metadata:raise BundleError('Export API returned no slides')
            for row in metadata:
                slide=row['index']; total=int(row['steps']); steps=range(total) if include_reveals else [total-1]
                for step in steps:
                    page.evaluate('''({slide,step,theme}) => {
                        const e=window.__presentationExport;
                        if(e) e.goto(slide,step);
                        else window.__deckDebug.navigate(slide,step,{fromUrl:true});
                        if(theme && ['signal','explainer','nocturne'].includes(theme)) {
                          document.querySelector('#stage').dataset.theme=theme;
                          const picker=document.querySelector('#theme-select');if(picker)picker.value=theme;
                        }
                    }''',{'slide':slide,'step':step,'theme':theme})
                    page.evaluate('''async()=>{await document.fonts.ready;
                        // Freeze continuous motion without making reveal elements disappear.
                        if(window.__presentationExport?.freeze)window.__presentationExport.freeze();
                    }''')
                    # Default poster snapshot for media should be visible without playback.
                    page.add_style_tag(content='@media print{*{animation:none!important;transition:none!important;scroll-behavior:auto!important} html,body{width:1600px!important;height:900px!important;overflow:hidden!important} #viewport{width:1600px!important;height:900px!important;position:fixed!important;left:0!important;top:0!important} #stage{position:absolute!important;left:0!important;top:0!important;transform:none!important;width:1600px!important;height:900px!important}}') if not frames else None
                    data=page.pdf(width='1600px',height='900px',print_background=True,prefer_css_page_size=False,margin={'top':'0','bottom':'0','left':'0','right':'0'})
                    reader=PdfReader(io.BytesIO(data))
                    if len(reader.pages)!=1:raise BundleError(f'Expected 1 PDF page, got {len(reader.pages)} for slide {slide+1}')
                    writer.add_page(reader.pages[0]);frames.append({'slide':slide+1,'step':step+1,'title':row['title']})
            if errors:raise BundleError('JavaScript exceptions in PDF run: '+'; '.join(errors))
        finally:browser.close()
    with open(destination,'wb') as f:writer.write(f)
    # Structural gate: exactly expected count, dimensions 16:9, nonblank file.
    result=PdfReader(str(destination))
    if len(result.pages)!=len(frames):raise BundleError('PDF page count mismatch')
    for i,page in enumerate(result.pages):
        w=float(page.mediabox.width);h=float(page.mediabox.height)
        if abs(w/h-16/9)>.003:raise BundleError(f'PDF page {i+1} aspect is {w/h:.4f}, not 16:9')
    return frames


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('deck',type=Path,help='Source directory containing index.html and local CSS/JS assets')
    ap.add_argument('--out',type=Path,required=True,help='Final output directory (only presentation.html and presentation.pdf)')
    ap.add_argument('--include-reveals',action='store_true',help='Export each progressive reveal as separate PDF page')
    ap.add_argument('--theme',choices=['signal','explainer','nocturne'],help='Override PDF export theme (HTML stays user-selectable)')
    ap.add_argument('--browser',help='Path to installed Chromium executable')
    args=ap.parse_args()
    try:
        if args.deck.resolve()==args.out.resolve():raise BundleError('Output must be distinct from source directory')
        bundled,stats=bundle_html(args.deck)
        out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
        html_path=out/'presentation.html'; pdf_path=out/'presentation.pdf'
        html_path.write_text(bundled,encoding='utf8')
        frames=write_pdf(bundled,pdf_path,args.include_reveals,args.theme,args.browser)
        print(json.dumps({'html':str(html_path),'pdf':str(pdf_path),'pages':len(frames),'frames':frames,'inlined':stats,'offline':True},indent=2))
        return 0
    except Exception as e:
        print(f'EXPORT ERROR: {e}',file=sys.stderr)
        return 1

if __name__=='__main__':sys.exit(main())
