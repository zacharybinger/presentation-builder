"""Optional example assertions for the unmodified starter. Adapt for your real widgets."""
from browser_support import frames, seek


def exercise(page,check):
    rows=frames(page)
    ids=page.evaluate('__deckDebug.scenes.map(s=>s.id)')
    seek(page,ids.index('explainer'),rows[ids.index('explainer')]['steps']-1)
    page.get_by_role('button',name='Inspect output node').click()
    check('Inspector updates explanation',page.locator('#inspect-label').inner_text()=='OUTPUT')
    seek(page,ids.index('experiment'),rows[ids.index('experiment')]['steps']-1)
    slider=page.get_by_role('slider',name='Minimum signal strength percentage')
    slider.fill('70')
    check('Threshold changes graph and count',page.locator('#retained-count').inner_text()=='1 / 3' and page.locator('.pathway.filtered').count()==2)
    page.get_by_role('button',name='RESET EXPERIMENT').click()
    check('Reset restores initial state',page.locator('#retained-count').inner_text()=='3 / 3')
    slider.focus(); before=page.evaluate('__deckDebug.state.step');page.keyboard.press('ArrowRight')
    check('Slider keys do not advance deck',page.evaluate('__deckDebug.state.step')==before)
