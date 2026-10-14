const TOTAL_STEPS = 9;

const steps = [
  {
    title: "A token’s meaning depends on its context.",
    copy: "The embedding for “it” starts without knowing what “it” refers to.",
    kicker: "Step 1 · Context",
    equation:
      '<span class="query-color">“it”</span> = ambiguous',
    detail:
      "The original token embedding is context-free. Self-attention lets this occurrence of “it” gather information from the surrounding sentence.",
    caption: "Which earlier words help explain “it”?",
  },
  {
    title: "Each token creates a query, key, and value.",
    copy: "These three learned projections give every token a role in the lookup.",
    kicker: "Step 2 · Q, K, V",
    equation:
      '<span class="query-color">Q</span> asks<br><span class="key-color">K</span> matches<br><span class="value-color">V</span> contributes',
    detail:
      "The focus token’s query is compared with every key. The corresponding values contain the information that can be carried forward.",
    caption: "The query from “it” will compare itself with every key.",
  },
  {
    title: "Attention scores decide what to gather.",
    copy: "Stronger query–key matches receive more weight.",
    kicker: "Step 3 · Score",
    equation:
      'score = <span class="query-color">Q</span> · <span class="key-color">K</span>',
    detail:
      "A softmax converts the raw scores into weights that add up to one. Here, “animal” receives the strongest connection.",
    caption: "Line thickness represents the attention weight from “it”.",
  },
  {
    title: "Values blend into a contextual embedding.",
    copy: "The weighted information becomes the next representation of “it”.",
    kicker: "Step 4 · Mix",
    equation:
      'softmax(<span class="query-color">Q</span><span class="key-color">Kᵀ</span>/√d)<span class="value-color">V</span>',
    detail:
      "The result still represents the token “it,” but now it carries sentence-specific information—especially that it refers to the animal.",
    caption: "Weighted values combine into a context-aware representation.",
  },
  {
    title: "Multiple heads can notice different relationships.",
    copy: "Parallel attention heads learn complementary patterns.",
    kicker: "Step 5 · Multi-head",
    equation:
      '<span class="attention-color">head₁ + head₂ + head₃ + …</span>',
    detail:
      "One head may track references, another grammar, and another nearby position. Their outputs are combined before the next layer.",
    caption: "Switch heads to see the same tokens organized for different purposes.",
  },
  {
    title: "Attention is one part of the prediction pipeline.",
    copy: "The contextual representation continues through every transformer block.",
    kicker: "Step 6 · Output head",
    equation:
      '<span class="attention-color">hidden state</span><br>→ vocabulary scores',
    detail:
      "After the final transformer block and normalization, a learned output projection produces one raw score for every token in the vocabulary.",
    caption: "The final hidden state is projected into vocabulary-sized logits.",
  },
  {
    title: "Logits become next-token probabilities.",
    copy: "Softmax turns raw vocabulary scores into a distribution that sums to one.",
    kicker: "Step 7 · Logits",
    equation:
      'P(token) = <span class="attention-color">softmax</span>(logits)',
    detail:
      "A logit is not yet a probability. Higher logits receive more probability after softmax, but the model has not selected a token yet.",
    caption: "Every vocabulary token receives a logit; only a few leading candidates are shown.",
  },
  {
    title: "Decoding controls shape the candidate pool.",
    copy: "Temperature changes sharpness; top-k and top-p remove unlikely options.",
    kicker: "Step 8 · Decode",
    equation:
      '<span class="query-color">temperature</span><br><span class="key-color">top-k</span> · <span class="value-color">top-p</span>',
    detail:
      "Temperature rescales all logits. Top-k keeps only the k highest candidates. Top-p keeps the smallest ranked set whose cumulative probability reaches p.",
    caption: "Change the controls and watch the eligible distribution update.",
  },
  {
    title: "The next token is sampled—not simply chosen.",
    copy: "One eligible token is drawn, appended, and the entire process repeats.",
    kicker: "Step 9 · Sample",
    equation:
      'distribution → <span class="attention-color">sample</span> → append → repeat',
    detail:
      "Greedy decoding always takes the highest probability. Sampling allows controlled variation: likely tokens win more often, but alternatives remain possible.",
    caption: "Sample repeatedly to see probability become an actual next-token decision.",
  },
];

const tokens = [
  { id: "the", label: "The", x: 92 },
  { id: "animal", label: "animal", x: 212 },
  { id: "was", label: "was", x: 336 },
  { id: "tired", label: "tired", x: 448 },
  { id: "so", label: "so", x: 552 },
  { id: "it", label: "it", x: 700 },
];

const heads = {
  reference: {
    label: "Reference head",
    result: "it → animal",
    weights: {
      the: 0.03,
      animal: 0.46,
      was: 0.07,
      tired: 0.27,
      so: 0.12,
      it: 0.05,
    },
  },
  grammar: {
    label: "Grammar head",
    result: "it → so",
    weights: {
      the: 0.02,
      animal: 0.08,
      was: 0.21,
      tired: 0.16,
      so: 0.48,
      it: 0.05,
    },
  },
  position: {
    label: "Position head",
    result: "it → nearby tokens",
    weights: {
      the: 0.01,
      animal: 0.04,
      was: 0.08,
      tired: 0.24,
      so: 0.42,
      it: 0.21,
    },
  },
};

const candidates = [
  { token: "rested", logit: 4.6 },
  { token: "slept", logit: 3.8 },
  { token: "stopped", logit: 2.9 },
  { token: "ran", logit: 2.4 },
  { token: "ate", logit: 1.6 },
  { token: "barked", logit: 0.9 },
];

const svgNamespace = "http://www.w3.org/2000/svg";
const tokenY = 168;
const tokenGroup = document.querySelector("#token-nodes");
const lineGroup = document.querySelector("#attention-lines");
const titleElement = document.querySelector("#slide-title");
const copyElement = document.querySelector("#step-copy");
const kickerElement = document.querySelector("#concept-kicker");
const equationElement = document.querySelector("#equation");
const detailElement = document.querySelector("#concept-detail");
const stageLabel = document.querySelector("#stage-label");
const stageCaption = document.querySelector("#stage-caption");
const previousButton = document.querySelector("#previous");
const nextButton = document.querySelector("#next");
const indicator = document.querySelector("#indicator");
const progressFill = document.querySelector("#progress-fill");
const headLabel = document.querySelector("#head-label");
const headResult = document.querySelector("#head-result");
const headButtons = [...document.querySelectorAll(".head-button")];
const candidateList = document.querySelector("#candidate-list");
const sampledToken = document.querySelector("#sampled-token");
const sampleButton = document.querySelector("#sample-button");
const temperatureButtons = [
  ...document.querySelectorAll("[data-temperature]"),
];
const topKButtons = [...document.querySelectorAll("[data-top-k]")];
const topPButtons = [...document.querySelectorAll("[data-top-p]")];
const lineElements = new Map();
const tokenElements = new Map();
let selectedHead = "reference";
let temperature = 1;
let topK = 5;
let topP = 0.95;
let filteredDistribution = [];

function createSvgElement(tag, attributes = {}) {
  const element = document.createElementNS(svgNamespace, tag);
  Object.entries(attributes).forEach(([key, value]) =>
    element.setAttribute(key, value),
  );
  return element;
}

function tokenWidth(label) {
  return Math.max(54, label.length * 9 + 24);
}

tokens.forEach((token, index) => {
  const width = tokenWidth(token.label);
  const isFocus = token.id === "it";
  const position = createSvgElement("g", {
    transform: `translate(${token.x} ${tokenY})`,
  });
  const group = createSvgElement("g", {
    class: `token-node${isFocus ? " focus" : ""}`,
    "data-token": token.id,
    style: `transition-delay: ${index * 45}ms`,
  });

  const box = createSvgElement("rect", {
    class: "token-box",
    x: -width / 2,
    y: -25,
    width,
    height: 50,
    rx: 12,
  });
  const text = createSvgElement("text", {
    class: "token-text",
    x: 0,
    y: 1,
  });
  text.textContent = token.label;
  group.append(box, text);

  const badgeY = 39;
  const keyBadge = createSvgElement("g", {
    class: "role-badge key",
    transform: "translate(-17 0)",
  });
  keyBadge.innerHTML =
    `<rect x="-13" y="${badgeY - 9}" width="26" height="18" rx="5"></rect>` +
    `<text x="0" y="${badgeY}">K</text>`;

  const valueBadge = createSvgElement("g", {
    class: "role-badge value",
    transform: "translate(17 0)",
  });
  valueBadge.innerHTML =
    `<rect x="-13" y="${badgeY - 9}" width="26" height="18" rx="5"></rect>` +
    `<text x="0" y="${badgeY}">V</text>`;

  group.append(keyBadge, valueBadge);

  if (isFocus) {
    const queryBadge = createSvgElement("g", {
      class: "role-badge query",
    });
    queryBadge.innerHTML =
      '<rect x="-13" y="-48" width="26" height="18" rx="5"></rect>' +
      '<text x="0" y="-39">Q</text>';
    group.appendChild(queryBadge);
  }

  position.appendChild(group);
  tokenGroup.appendChild(position);
  tokenElements.set(token.id, group);
});

const focusToken = tokens.find((token) => token.id === "it");

tokens.forEach((token) => {
  if (token.id === "it" || token.masked) return;
  const midpoint = (focusToken.x + token.x) / 2;
  const distance = Math.abs(focusToken.x - token.x);
  const controlY = Math.max(38, 126 - distance * 0.13);
  const path = createSvgElement("path", {
    class: "attention-path",
    "data-token": token.id,
    d: `M ${focusToken.x} ${tokenY - 28} Q ${midpoint} ${controlY} ${token.x} ${tokenY - 28}`,
  });
  lineGroup.appendChild(path);
  lineElements.set(token.id, path);
});

candidates.forEach((candidate) => {
  const row = document.createElement("div");
  row.className = "candidate-row";
  row.dataset.token = candidate.token;
  row.innerHTML =
    `<code>${candidate.token}</code>` +
    `<div class="candidate-track"><i></i></div>` +
    `<span class="candidate-probability">0%</span>`;
  candidateList.appendChild(row);
});

function readStepFromUrl() {
  const value = Number(new URLSearchParams(window.location.search).get("step"));
  return Number.isInteger(value) && value >= 1 && value <= TOTAL_STEPS
    ? value
    : 1;
}

let currentStep = readStepFromUrl();

function renderHead(headId) {
  selectedHead = headId;
  const head = heads[headId];
  const strongest = Object.entries(head.weights)
    .filter(([id]) => id !== "it")
    .sort((a, b) => b[1] - a[1])[0][0];

  lineElements.forEach((line, tokenId) => {
    const weight = head.weights[tokenId];
    line.style.strokeWidth = String(1 + weight * 12);
    line.style.setProperty("--line-opacity", String(0.18 + weight * 1.65));
    line.classList.toggle("strongest", tokenId === strongest);
    line.classList.toggle(
      "visible",
      currentStep >= 3 && currentStep <= 5,
    );
  });

  tokenElements.forEach((element, tokenId) => {
    element.classList.toggle(
      "attended",
      tokenId === strongest && currentStep >= 3 && currentStep <= 5,
    );
  });

  headButtons.forEach((button) => {
    const active = button.dataset.head === headId;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  headLabel.textContent = head.label;
  headResult.textContent = head.result;
}

function softmax(values) {
  const max = Math.max(...values);
  const exponents = values.map((value) => Math.exp(value - max));
  const total = exponents.reduce((sum, value) => sum + value, 0);
  return exponents.map((value) => value / total);
}

function computeDistribution() {
  const probabilities = softmax(
    candidates.map((candidate) => candidate.logit / temperature),
  );
  const ranked = candidates.map((candidate, index) => ({
    ...candidate,
    probability: probabilities[index],
    eligible: false,
    finalProbability: 0,
  }));

  const topKSet = ranked.slice(0, topK);
  const topKTotal = topKSet.reduce(
    (sum, candidate) => sum + candidate.probability,
    0,
  );
  let cumulative = 0;
  const nucleus = [];

  for (const candidate of topKSet) {
    const normalized = candidate.probability / topKTotal;
    nucleus.push(candidate);
    cumulative += normalized;
    if (cumulative >= topP) break;
  }

  const nucleusTotal = nucleus.reduce(
    (sum, candidate) => sum + candidate.probability,
    0,
  );
  nucleus.forEach((candidate) => {
    candidate.eligible = true;
    candidate.finalProbability = candidate.probability / nucleusTotal;
  });
  return ranked;
}

function renderDistribution() {
  filteredDistribution = computeDistribution();
  const maxProbability = Math.max(
    ...filteredDistribution.map((candidate) => candidate.finalProbability),
  );

  filteredDistribution.forEach((candidate) => {
    const row = candidateList.querySelector(
      `[data-token="${candidate.token}"]`,
    );
    const bar = row.querySelector(".candidate-track i");
    const probability = row.querySelector(".candidate-probability");
    row.classList.toggle("filtered", !candidate.eligible);
    bar.style.width = candidate.eligible
      ? `${(candidate.finalProbability / maxProbability) * 100}%`
      : "0%";
    probability.textContent = candidate.eligible
      ? `${Math.round(candidate.finalProbability * 100)}%`
      : "filtered";
  });
}

function sampleNextToken() {
  const eligible = filteredDistribution.filter(
    (candidate) => candidate.eligible,
  );
  let draw = Math.random();
  let chosen = eligible[eligible.length - 1];
  for (const candidate of eligible) {
    draw -= candidate.finalProbability;
    if (draw <= 0) {
      chosen = candidate;
      break;
    }
  }

  sampledToken.textContent = chosen.token;
  sampledToken.classList.remove("sampled");
  requestAnimationFrame(() => sampledToken.classList.add("sampled"));
  candidateList
    .querySelectorAll(".candidate-row")
    .forEach((row) =>
      row.classList.toggle("chosen", row.dataset.token === chosen.token),
    );
}

function activateControl(buttons, activeButton) {
  buttons.forEach((button) =>
    button.classList.toggle("active", button === activeButton),
  );
}

function render(step, { updateHistory = true } = {}) {
  currentStep = Math.max(1, Math.min(TOTAL_STEPS, step));
  const content = steps[currentStep - 1];

  document.body.dataset.step = String(currentStep);
  titleElement.textContent = content.title;
  copyElement.textContent = content.copy;
  kickerElement.textContent = content.kicker;
  equationElement.innerHTML = content.equation;
  detailElement.textContent = content.detail;
  stageLabel.textContent =
    currentStep >= 6 ? "Next-token decoding" : "A single attention operation";
  stageCaption.textContent = content.caption;

  tokenElements.forEach((element) => element.classList.add("visible"));
  renderHead(selectedHead);
  renderDistribution();
  if (currentStep === 9 && sampledToken.textContent === "?") {
    sampleNextToken();
  }

  previousButton.disabled = currentStep === 1;
  nextButton.disabled = currentStep === TOTAL_STEPS;
  indicator.textContent = `${currentStep} / ${TOTAL_STEPS}`;
  progressFill.style.width = `${(currentStep / TOTAL_STEPS) * 100}%`;

  if (updateHistory) {
    const url = new URL(window.location.href);
    url.searchParams.set("step", String(currentStep));
    window.history.pushState({ step: currentStep }, "", url);
  }
}

function goTo(step) {
  if (step === currentStep || step < 1 || step > TOTAL_STEPS) return;
  render(step);
}

previousButton.addEventListener("click", (event) => {
  event.stopPropagation();
  goTo(currentStep - 1);
});

nextButton.addEventListener("click", (event) => {
  event.stopPropagation();
  goTo(currentStep + 1);
});

headButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    renderHead(button.dataset.head);
  });
});

temperatureButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    temperature = Number(button.dataset.temperature);
    activateControl(temperatureButtons, button);
    sampledToken.textContent = "?";
    renderDistribution();
  });
});

topKButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    topK = Number(button.dataset.topK);
    activateControl(topKButtons, button);
    sampledToken.textContent = "?";
    renderDistribution();
  });
});

topPButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    topP = Number(button.dataset.topP);
    activateControl(topPButtons, button);
    sampledToken.textContent = "?";
    renderDistribution();
  });
});

sampleButton.addEventListener("click", (event) => {
  event.stopPropagation();
  sampleNextToken();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === " ") {
    event.preventDefault();
    goTo(currentStep + 1);
  } else if (event.key === "ArrowLeft") {
    event.preventDefault();
    goTo(currentStep - 1);
  } else if (event.key === "Home") {
    event.preventDefault();
    goTo(1);
  } else if (event.key === "End") {
    event.preventDefault();
    goTo(TOTAL_STEPS);
  }
});

document.querySelector(".attention-shell").addEventListener("click", (event) => {
  if (event.target.closest("button, a")) return;
  goTo(currentStep + 1);
});

window.addEventListener("popstate", () => {
  render(readStepFromUrl(), { updateHistory: false });
});

render(currentStep, { updateHistory: false });
