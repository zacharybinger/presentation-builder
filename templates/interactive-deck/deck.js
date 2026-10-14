/* Presentation Builder example content and shared controller.
 * Replace scenes[] with your subject-specific storyline. One persistent scene per
 * slide, one idea per reveal. The input→transformation→output demonstration below
 * is schematic/illustrative, NOT a benchmark or physical simulation.
 */
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
const scenes = [
  {
    id: 'premise', nav: 'Premise', eyebrow: 'THE PREMISE',
    title: 'Ideas deserve <em>to be felt.</em>',
    steps: [
      'A presentation can be more than a sequence of screens. It can be a place to discover.',
      'Give the audience a mental model they can see, test, and remember.'
    ],
    html: `
      <div class="opening-scene">
        <div class="opening-statement">
          <div class="opening-number">01 — THE NEW FORMAT</div>
          <p class="opening-quote">A little less<br>explaining.<br><span>A lot more</span><br>understanding.</p>
          <div class="small-rule"></div>
          <p class="opening-caption">Build an interactive argument—not a stack of static cards.</p>
        </div>
        <div class="hero-art" role="img" aria-label="Nested concentric circles with a bright highlighted center, representing an idea becoming clear">
          <div class="orbit orbit-a"></div><div class="orbit orbit-b"></div><div class="orbit orbit-c"></div>
          <div class="orbit-point point-one"></div><div class="orbit-point point-two"></div>
          <div class="hero-core">AHA<span>!</span></div>
          <div class="art-label art-label-top">FROM CONTEXT</div><div class="art-label art-label-bottom">TO CLARITY ↗</div>
          <div class="progressive hero-annotation" data-at="1">Every layer makes the same idea clearer.</div>
        </div>
      </div>`
  },
  {
    id: 'structure', nav: 'Structure', eyebrow: 'STORY AS SYSTEM',
    title: 'One idea. <em>Four transformations.</em>',
    steps: [
      'Start with the source material, not a preselected slide template.',
      'Organize context into claims and evidence.',
      'Reveal relationships when the audience needs them.',
      'End with a change in understanding—not just another slide.'
    ],
    html: `
      <div class="flow-scene">
        <div class="flow-tag">A NARRATIVE PIPELINE / INTERACTIVE</div>
        <div class="flow-tray">
          <div class="flow-card progressive" data-at="0"><span class="flow-num">01</span><span class="flow-icon">≡</span><strong>CONTEXT</strong><small>Words, evidence,<br>constraints</small></div>
          <div class="flow-link progressive" data-at="1"><i></i></div>
          <div class="flow-card flow-blue progressive" data-at="1"><span class="flow-num">02</span><span class="flow-icon">⌘</span><strong>STRUCTURE</strong><small>Claims, sequence,<br>meaning</small></div>
          <div class="flow-link progressive" data-at="2"><i></i></div>
          <div class="flow-card flow-orange progressive" data-at="2"><span class="flow-num">03</span><span class="flow-icon">✦</span><strong>REVEAL</strong><small>Motion, interaction,<br>comparison</small></div>
          <div class="flow-link progressive" data-at="3"><i></i></div>
          <div class="flow-card flow-ink progressive" data-at="3"><span class="flow-num">04</span><span class="flow-icon">↗</span><strong>INSIGHT</strong><small>Memorable, useful,<br>explainable</small></div>
        </div>
        <div class="flow-baseline"><span>READ LEFT TO RIGHT</span><span>STRUCTURE IS A COGNITIVE TOOL, NOT A DECORATION</span></div>
        <div class="flow-footer progressive" data-at="3"><b>Every new reveal should change the audience's mental model.</b><span>Keep the objects. Transform their meaning.</span></div>
      </div>`
  },
  {
    id: 'explainer', nav: 'Anatomy', eyebrow: 'THE EXPLAINER PATTERN',
    title: 'Show the mechanism, <em>then inspect it.</em>',
    steps: [
      'A single diagram provides the shared reference point.',
      'Reveal the connections, not a fresh drawing.',
      'Expose the transformation and its result.',
      'Let the audience inspect a component to reinforce the model.'
    ],
    html: `
      <div class="anatomy-scene">
        <div class="diagram-paper">
          <div class="diagram-overline"><span>02 / SYSTEM ANATOMY</span><span>SIMPLIFIED EXAMPLE</span></div>
          <div class="network-track" aria-label="Three-stage model: input, transformation, output">
            <div class="network-node node-input"><button type="button" data-node="input" class="node-button" aria-label="Inspect input node"><span>INPUT</span><strong>01</strong><small>raw signal</small></button></div>
            <div class="network-edge progressive" data-at="1"><span class="edge-line"></span><span class="edge-label">encoding</span></div>
            <div class="network-node progressive" data-at="1"><button type="button" data-node="process" class="node-button node-process" aria-label="Inspect transform node"><span>PROCESS</span><strong>02</strong><small>weighted mix</small></button></div>
            <div class="network-edge progressive" data-at="2"><span class="edge-line"></span><span class="edge-label">inference</span></div>
            <div class="network-node progressive" data-at="2"><button type="button" data-node="output" class="node-button node-output" aria-label="Inspect output node"><span>OUTPUT</span><strong>03</strong><small>interpreted result</small></button></div>
          </div>
          <div class="network-underlay"><span class="network-tick">BEGIN</span><span class="network-tick">TRANSFORM</span><span class="network-tick">CONCLUDE</span></div>
          <div class="progressive detail-note" data-at="3">CLICK THE NODES ABOVE TO INSPECT THEIR ROLES ↑</div>
        </div>
        <aside class="diagram-detail" data-no-advance>
          <span class="side-index">OBJECT INSPECTOR / 01</span>
          <div class="detail-glyph" aria-hidden="true">◈</div>
          <span class="side-label">SELECTED ROLE</span>
          <strong id="inspect-label">INPUT</strong>
          <p id="inspect-copy" aria-live="polite">Information enters the model in a representation it can process.</p>
          <div class="side-foot">EXPLORE A RELATIONSHIP<br>WITHOUT LOSING CONTEXT</div>
        </aside>
      </div>`
  },
  {
    id: 'experiment', nav: 'Experiment', eyebrow: 'A LIVE EXPERIMENT',
    title: 'Turn the picture <em>into a question.</em>',
    steps: [
      'The audience sees a relationship, not just a diagram.',
      'Adjust the threshold to choose which signal pathways remain visible.',
      'Use the result to discuss tradeoffs; the values here are illustrative.'
    ],
    html: `
      <div class="lab-scene">
        <div class="lab-visual">
          <div class="lab-top"><span>INTERACTIVE DEMO / NOT MEASURED DATA</span><span>PATHWAY FILTER</span></div>
          <svg viewBox="0 0 780 350" class="lab-network" role="img" aria-label="Three connections of illustrative strengths 91, 63 and 37 percent, updated by the threshold slider">
            <defs><marker id="lab-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>
            <rect x="34" y="124" width="126" height="90" rx="20" class="lab-node source-node"/><text x="97" y="162" class="lab-text">INPUT</text><text x="97" y="190" class="lab-id">S</text>
            <g class="pathway" data-strength="91"><path d="M 164 152 C 290 152 305 46 423 46"/><rect x="425" y="12" width="160" height="72" rx="18"/><text x="505" y="42" class="lab-text">PATH A</text><text x="505" y="64" class="lab-small">91% strength</text></g>
            <g class="pathway" data-strength="63"><path d="M 164 169 L 423 169"/><rect x="425" y="133" width="160" height="72" rx="18"/><text x="505" y="163" class="lab-text">PATH B</text><text x="505" y="185" class="lab-small">63% strength</text></g>
            <g class="pathway" data-strength="37"><path d="M 164 186 C 290 186 305 289 423 289"/><rect x="425" y="253" width="160" height="72" rx="18"/><text x="505" y="283" class="lab-text">PATH C</text><text x="505" y="305" class="lab-small">37% strength</text></g>
            <text x="32" y="316" class="lab-axis">INCREASING FILTER → FEWER PATHWAYS</text>
          </svg>
          <div class="lab-meter"><span>SIGNAL RETAINED</span><strong id="retained-count">3 / 3</strong><div class="lab-meter-track"><i id="retained-bar" style="width:100%"></i></div></div>
        </div>
        <div class="lab-panel" data-no-advance>
          <div class="lab-index">CONTROL ROOM <span>LIVE</span></div>
          <label for="threshold" class="lab-label">MINIMUM STRENGTH</label>
          <div class="lab-number"><strong id="threshold-display">20</strong><span>%</span></div>
          <input id="threshold" type="range" min="0" max="100" step="1" value="20" aria-label="Minimum signal strength percentage" />
          <div class="scale-labels"><span>0%</span><span>100%</span></div>
          <div class="progressive lab-result" data-at="1"><span class="result-kicker">OBSERVATION</span><p id="lab-outcome" aria-live="polite">All three pathways remain visible at this threshold.</p><button id="reset-threshold" type="button" class="reset-button">↺ RESET EXPERIMENT</button></div>
        </div>
      </div>`
  },
  {
    id: 'takeaway', nav: 'Takeaway', eyebrow: 'THE TAKEAWAY',
    title: 'Build the understanding. <em>Not just the slides.</em>',
    steps: [
      'Make the content accurate and the visual language coherent.',
      'Use interaction where it changes what the audience can discover.',
      'Test the real browser. Then put the story on stage.'
    ],
    html: `
      <div class="takeaway-scene">
        <div class="takeaway-main">
          <div class="takeaway-orbit" aria-hidden="true"><span>✳</span></div>
          <span class="takeaway-label">A REUSABLE PRESENTATION PRINCIPLE</span>
          <blockquote>Make every<br><em>interaction</em><br>matter.</blockquote>
          <span class="takeaway-base">STORY <i>✳</i> SYSTEM <i>✳</i> EXPERIENCE</span>
        </div>
        <div class="takeaway-side">
          <div class="takeaway-line progressive" data-at="0"><span>01</span><strong>CLARIFY</strong><small>One message per scene.</small></div>
          <div class="takeaway-line progressive" data-at="1"><span>02</span><strong>INTERACT</strong><small>Make a relationship tangible.</small></div>
          <div class="takeaway-line progressive" data-at="2"><span>03</span><strong>VERIFY</strong><small>Ship what works in a browser.</small></div>
        </div>
      </div>`
  }
];

const state = { slide: 0, step: 0, theme: '__DEFAULT_THEME__' };
const $ = sel => document.querySelector(sel);
const stage = $('#stage');
const content = $('#scene-root');
const chapterNav = $('#chapter-nav');
const pct = $('#progress-fill');
const totalReveals = scenes.reduce((n, scene) => n + scene.steps.length, 0);

function readUrl() {
  const params = new URLSearchParams(location.search);
  const requestedSlide = Number(params.get('slide') ?? 1);
  const slide = Number.isFinite(requestedSlide) ? clamp(Math.trunc(requestedSlide) - 1, 0, scenes.length - 1) : 0;
  const requestedStep = Number(params.get('step') ?? 1);
  const step = Number.isFinite(requestedStep) ? clamp(Math.trunc(requestedStep) - 1, 0, scenes[slide].steps.length - 1) : 0;
  const theme = ['signal', 'explainer', 'nocturne'].includes(params.get('theme')) ? params.get('theme') : '__DEFAULT_THEME__';
  return { slide, step, theme };
}
function writeUrl(mode = 'push') {
  const url = new URL(location.href);
  url.searchParams.set('slide', String(state.slide + 1));
  url.searchParams.set('step', String(state.step + 1));
  url.searchParams.set('theme', state.theme);
  history[mode === 'replace' ? 'replaceState' : 'pushState']({ ...state }, '', url);
}
function applyScale() {
  const scale = Math.min(innerWidth / 1600, innerHeight / 900);
  stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
}
function renderNavigation() {
  chapterNav.innerHTML = scenes.map((scene, i) => `<button type="button" class="chapter-button${i === state.slide ? ' is-current' : ''}" data-chapter="${i}" aria-label="Go to ${scene.nav}" ${i === state.slide ? 'aria-current="step"' : ''}>${String(i + 1).padStart(2, '0')} <span>${scene.nav}</span></button>`).join('');
  chapterNav.querySelectorAll('[data-chapter]').forEach(button => button.addEventListener('click', () => navigate(Number(button.dataset.chapter), 0)));
}
function renderScene() {
  const scene = scenes[state.slide];
  $('#chapter-number').textContent = String(state.slide + 1).padStart(2, '0');
  $('#eyebrow-text').textContent = scene.eyebrow;
  $('#slide-heading').innerHTML = scene.title; // Trusted static scene configuration; do not use for untrusted text.
  content.innerHTML = scene.html;                // Trusted static scene configuration only.
  content.dataset.scene = scene.id;
  renderNavigation();
  wireWidgets(scene.id);
}
function renderStep() {
  const scene = scenes[state.slide];
  $('#step-copy').textContent = scene.steps[state.step];
  content.querySelectorAll('[data-at]').forEach(el => {
    const visible = state.step >= Number(el.dataset.at);
    el.classList.toggle('is-visible', visible);
    el.inert = !visible;
    el.setAttribute('aria-hidden', String(!visible));
  });
  $('#previous').disabled = state.slide === 0 && state.step === 0;
  $('#next').disabled = state.slide === scenes.length - 1 && state.step === scene.steps.length - 1;
  const completed = scenes.slice(0, state.slide).reduce((n, x) => n + x.steps.length, 0) + state.step + 1;
  pct.style.width = `${100 * completed / totalReveals}%`;
  $('#progress-label').textContent = `${String(state.slide + 1).padStart(2,'0')} / ${String(scenes.length).padStart(2,'0')} · ${state.step + 1}/${scene.steps.length}`;
  stage.dataset.step = String(state.step);
}
function navigate(slide, step, options = {}) {
  const targetSlide = clamp(slide, 0, scenes.length - 1);
  const targetStep = clamp(step, 0, scenes[targetSlide].steps.length - 1);
  const changedSlide = state.slide !== targetSlide;
  state.slide = targetSlide; state.step = targetStep;
  if (changedSlide || options.initial) renderScene();
  renderStep();
  if (!options.fromUrl) writeUrl(options.initial ? 'replace' : 'push');
}
function advance(direction) {
  const nextStep = state.step + direction;
  if (nextStep >= 0 && nextStep < scenes[state.slide].steps.length) navigate(state.slide, nextStep);
  else if (direction > 0 && state.slide < scenes.length - 1) navigate(state.slide + 1, 0);
  else if (direction < 0 && state.slide > 0) navigate(state.slide - 1, scenes[state.slide - 1].steps.length - 1);
}
function updateTheme(theme) {
  if (!['signal','explainer','nocturne'].includes(theme)) return;
  state.theme = theme;
  stage.dataset.theme = theme;
  $('#theme-select').value = theme;
  writeUrl('replace');
}
function wireWidgets(id) {
  if (id === 'explainer') {
    const definitions = {
      input: ['INPUT', 'Information enters the model in a representation it can process.', '01'],
      process: ['PROCESS', 'An explicit transformation operates on the incoming signal. The formula is omitted here for clarity.', '02'],
      output: ['OUTPUT', 'A result emerges. Its meaning depends on the context and the transformation used.', '03']
    };
    content.querySelectorAll('[data-node]').forEach(button => button.addEventListener('click', () => {
      const [label, copy, index] = definitions[button.dataset.node];
      $('#inspect-label').textContent = label;
      $('#inspect-copy').textContent = copy;
      $('.side-index').textContent = `OBJECT INSPECTOR / ${index}`;
      content.querySelectorAll('[data-node]').forEach(b => b.classList.toggle('selected', b === button));
    }));
  }
  if (id === 'experiment') {
    const slider = $('#threshold');
    const update = () => {
      const v = Number(slider.value);
      const selected = [...content.querySelectorAll('.pathway')].map(el => ({ el, strength: Number(el.dataset.strength) }));
      const count = selected.filter(x => x.strength >= v).length;
      selected.forEach(({el,strength}) => el.classList.toggle('filtered', strength < v));
      $('#threshold-display').textContent = v;
      $('#retained-count').textContent = `${count} / 3`;
      $('#retained-bar').style.width = `${count * 100 / 3}%`;
      $('#lab-outcome').textContent = count === 3 ? 'All three pathways remain visible at this threshold.' : count === 0 ? 'No pathways exceed the chosen threshold.' : `Only ${count} of three pathways meet the threshold.`;
      slider.setAttribute('aria-valuetext', `${v} percent, ${count} connections retained`);
    };
    slider.addEventListener('input', update);
    $('#reset-threshold').addEventListener('click', () => { slider.value = '20'; update(); });
    update();
  }
}

$('#previous').addEventListener('click', () => advance(-1));
$('#next').addEventListener('click', () => advance(1));
$('#theme-select').addEventListener('change', e => updateTheme(e.target.value));
$('#fullscreen').addEventListener('click', async () => {
  try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); }
  catch (error) { console.warn('Fullscreen unavailable:', error); }
});
// Only advance on truly noninteractive stage clicks, preserving selection and controls.
stage.addEventListener('click', event => {
  if (event.target.closest('button,a,input,select,textarea,[data-no-advance],label,[role="slider"]')) return;
  if (window.getSelection()?.toString()) return;
  advance(1);
});
document.addEventListener('keydown', event => {
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  if (event.target.closest('button,a,input,select,textarea,[contenteditable="true"],[role="slider"]')) return;
  if (event.key === 'ArrowRight' || event.key === ' ' || event.key === 'PageDown') { event.preventDefault(); advance(1); }
  else if (event.key === 'ArrowLeft' || event.key === 'PageUp') { event.preventDefault(); advance(-1); }
  else if (event.key === 'Home') { event.preventDefault(); navigate(0,0); }
  else if (event.key === 'End') { event.preventDefault(); navigate(scenes.length - 1,scenes[scenes.length - 1].steps.length - 1); }
  else if (event.key.toLowerCase() === 'f' && !event.repeat) $('#fullscreen').click();
});
window.addEventListener('popstate', () => {
  const target = readUrl();
  const themeChanged = target.theme !== state.theme;
  state.theme = target.theme;
  if (themeChanged) { stage.dataset.theme = state.theme; $('#theme-select').value = state.theme; }
  navigate(target.slide, target.step, { fromUrl: true });
});
window.addEventListener('resize', applyScale, { passive: true });
const initial = readUrl(); state.theme = initial.theme;
stage.dataset.theme = state.theme; $('#theme-select').value = state.theme;
applyScale(); navigate(initial.slide, initial.step, { initial: true, fromUrl: true });
window.__deckDebug = { scenes, state, navigate, advance, get totalReveals() { return totalReveals; } };
// Portable publishing interface: direct seek to a slide/reveal and freeze for PDF.
// The HTML retains live widgets; the PDF exporter only visits a representative still.
window.__presentationExport = {
  frames: () => scenes.map((s,index) => ({ index, steps:s.steps.length, title:s.nav||s.id })),
  goto: (slide,step) => navigate(slide,step,{fromUrl:true}),
  freeze: () => { /* No continuous JS animation in the default starter. */ }
};
