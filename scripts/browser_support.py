"""Shared browser/export contract. No presentation-specific content assumptions."""
from pathlib import Path


def launch_browser(playwright, executable=None):
    options = {'headless': True}
    if executable:
        options['executable_path'] = executable
    return playwright.chromium.launch(**options)


def frames(page):
    page.wait_for_function('Boolean(window.__presentationExport || window.__deckDebug)')
    rows = page.evaluate('''() => window.__presentationExport?.frames() ||
        window.__deckDebug.scenes.map((s,index)=>({index,steps:s.steps.length,title:s.nav||s.id}))''')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Export frames() must return a nonempty array')
    for index, row in enumerate(rows):
        if (not isinstance(row, dict) or type(row.get('index')) is not int
                or row['index'] != index or type(row.get('steps')) is not int
                or row['steps'] < 1 or not isinstance(row.get('title'), str)):
            raise ValueError('Each frame needs consecutive zero-based index, positive integer steps, and string title')
    return rows


def seek(page, index, step):
    page.evaluate('''async ({index,step}) => {
        if(window.__presentationExport) await window.__presentationExport.goto(index,step);
        else window.__deckDebug.navigate(index,step,{fromUrl:true});
        await document.fonts.ready;
        await Promise.all([...document.images].map(img => img.decode().catch(()=>{})));
        await new Promise(resolve => requestAnimationFrame(()=>requestAnimationFrame(resolve)));
    }''', {'index': index, 'step': step})


def stage_fits(page):
    return page.evaluate('''() => {
      const stage=document.querySelector('#stage');
      if(!stage) return {ok:false,reason:'Export contract requires #stage'};
      const b=stage.getBoundingClientRect();
      return {ok:b.width>0 && b.height>0 && Math.abs(b.width/b.height-16/9)<.003 &&
        b.x>=-1 && b.y>=-1 && b.right<=innerWidth+1 && b.bottom<=innerHeight+1,
        x:b.x,y:b.y,width:b.width,height:b.height};
    }''')


def content_overflow(page):
    # Look for clipped text and controls, not intentional decorative bleeds.
    return page.evaluate('''() => {
      const stage=document.querySelector('#stage'); if(!stage)return ['missing #stage'];
      const b=stage.getBoundingClientRect();
      return [...stage.querySelectorAll('h1,h2,h3,p,button,select,label,svg text,[data-check-bounds]')]
        .filter(el=>!el.closest('[aria-hidden="true"],[data-allow-overflow]'))
        .filter(el=>{const s=getComputedStyle(el);return s.display!=='none' && s.visibility!=='hidden' && s.opacity!=='0';})
        .filter(el=>{const r=el.getBoundingClientRect();return r.width && r.height &&
          (r.left<b.left-2 || r.right>b.right+2 || r.top<b.top-2 || r.bottom>b.bottom+2 ||
          (el.namespaceURI!== 'http://www.w3.org/2000/svg' &&
           ((['hidden','clip','auto','scroll'].includes(getComputedStyle(el).overflowX) && el.scrollWidth>el.clientWidth+2) ||
            (['hidden','clip','auto','scroll'].includes(getComputedStyle(el).overflowY) && el.scrollHeight>el.clientHeight+2))));})
        .map(el=>(el.id||el.tagName)+': '+el.textContent.trim().slice(0,80));
    }''')


def contact_sheet(out, names):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    tiles=[]
    for name in names:
        if name.startswith('mobile'): continue
        with Image.open(Path(out)/name) as source:
            img=source.convert('RGB'); img.thumbnail((640,360))
            tile=Image.new('RGB',(660,390),'white')
            tile.paste(img,((660-img.width)//2,8))
            ImageDraw.Draw(tile).text((12,370),name,fill='#19283c')
            tiles.append(tile)
    if tiles:
        sheet=Image.new('RGB',(1320,((len(tiles)+1)//2)*390),'#e8edf4')
        for i,tile in enumerate(tiles):sheet.paste(tile,((i%2)*660,(i//2)*390))
        sheet.save(Path(out)/'contact-sheet.png')
