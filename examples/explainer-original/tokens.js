const TOTAL_STEPS = 5;

const steps = [
  {
    title: "Language becomes pieces a model can process.",
    copy: "A tokenizer splits text into reusable fragments and assigns each one an ID.",
    kicker: "Step 1 · Tokenize",
    equation:
      'text → <span class="token-color">tokens</span> → IDs',
    detail:
      "Models do not read words directly. They receive a sequence of integer token IDs. Common fragments may be whole words; uncommon words may become several pieces.",
  },
  {
    title: "Every token ID retrieves a vector.",
    copy: "An embedding converts a discrete symbol into a trainable list of numbers.",
    kicker: "Step 2 · Embed",
    equation:
      'ID → <span class="vector-color">[0.82, −0.14, …]</span>',
    detail:
      "A token ID alone contains no useful geometry. Its embedding gives the network continuous numbers it can combine, compare, and update during training.",
  },
  {
    title: "Meaning emerges as geometry.",
    copy: "Training places tokens used in similar contexts near similar directions.",
    kicker: "Step 3 · Embedding space",
    equation:
      '<span class="vector-color">similar context</span><br>≈ nearby vectors',
    detail:
      "The plot is a simplified 2D projection. Real embedding vectors can have hundreds or thousands of dimensions.",
  },
  {
    title: "Cosine similarity compares directions.",
    copy: "A small angle means two embedding vectors point in similar directions.",
    kicker: "Step 4 · Compare",
    equation:
      '<span class="cosine-color">cos(θ)</span> = (a · b) / (‖a‖‖b‖)',
    detail:
      "Cosine similarity focuses on direction rather than raw vector length. Similar tokens tend toward 1; unrelated directions tend toward 0.",
  },
  {
    title: "Embeddings give language a usable shape.",
    copy: "The network can now operate on relationships—not merely token IDs.",
    kicker: "Step 5 · Why it matters",
    equation:
      'symbols → <span class="vector-color">geometry</span> → computation',
    detail:
      "Embeddings are learned, task-dependent coordinates. They provide a useful starting representation; later transformer layers continually refine it using context.",
  },
];

const points = [
  { id: "cat", label: "cat", category: "animals", x: 665, y: 78 },
  { id: "dog", label: "dog", category: "animals", x: 630, y: 105 },
  { id: "puppy", label: "puppy", category: "animals", x: 690, y: 122 },
  { id: "kitten", label: "kitten", category: "animals", x: 735, y: 91 },
  { id: "truck", label: "truck", category: "vehicles", x: 585, y: 238 },
  { id: "car", label: "car", category: "vehicles", x: 635, y: 252 },
  { id: "bus", label: "bus", category: "vehicles", x: 680, y: 228 },
  { id: "apple", label: "apple", category: "fruit", x: 370, y: 75 },
  { id: "orange", label: "orange", category: "fruit", x: 420, y: 105 },
  { id: "banana", label: "banana", category: "fruit", x: 455, y: 68 },
  { id: "king", label: "king", category: "royalty", x: 205, y: 116 },
  { id: "queen", label: "queen", category: "royalty", x: 248, y: 83 },
  { id: "prince", label: "prince", category: "royalty", x: 275, y: 133 },
];

const comparisons = {
  dog: { score: "0.94", className: "similar" },
  truck: { score: "0.18", className: "different" },
};

const svgNamespace = "http://www.w3.org/2000/svg";
const origin = { x: 80, y: 285 };
const pointGroup = document.querySelector("#plot-points");
const vectorGroup = document.querySelector("#comparison-vectors");
const titleElement = document.querySelector("#slide-title");
const copyElement = document.querySelector("#step-copy");
const kickerElement = document.querySelector("#concept-kicker");
const equationElement = document.querySelector("#equation");
const detailElement = document.querySelector("#concept-detail");
const previousButton = document.querySelector("#previous");
const nextButton = document.querySelector("#next");
const indicator = document.querySelector("#indicator");
const progressFill = document.querySelector("#progress-fill");
const scoreElement = document.querySelector("#similarity-score");
const pairButtons = [...document.querySelectorAll(".pair-button")];
const pointElements = new Map();

function createSvgElement(tag, attributes = {}) {
  const element = document.createElementNS(svgNamespace, tag);
  Object.entries(attributes).forEach(([key, value]) =>
    element.setAttribute(key, value),
  );
  return element;
}

points.forEach((point, index) => {
  const position = createSvgElement("g", {
    transform: `translate(${point.x} ${point.y})`,
  });
  const group = createSvgElement("g", {
    class: `plot-point ${point.category}`,
    "data-point": point.id,
    style: `transition-delay: ${index * 35}ms`,
  });
  const radius = Math.max(22, point.label.length * 4 + 10);
  const circle = createSvgElement("circle", { r: radius });
  const label = createSvgElement("text", { x: 0, y: 1 });
  label.textContent = point.label;
  group.append(circle, label);
  position.appendChild(group);
  pointGroup.appendChild(position);
  pointElements.set(point.id, group);
});

const baseVector = createSvgElement("line", {
  class: "comparison-vector base",
  x1: origin.x,
  y1: origin.y,
  x2: points.find((point) => point.id === "cat").x,
  y2: points.find((point) => point.id === "cat").y,
});

const targetVector = createSvgElement("line", {
  class: "comparison-vector target similar",
  x1: origin.x,
  y1: origin.y,
});

vectorGroup.append(baseVector, targetVector);

let selectedTarget = "dog";

function readStepFromUrl() {
  const value = Number(new URLSearchParams(window.location.search).get("step"));
  return Number.isInteger(value) && value >= 1 && value <= TOTAL_STEPS
    ? value
    : 1;
}

let currentStep = readStepFromUrl();

function renderComparison(targetId) {
  selectedTarget = targetId;
  const target = points.find((point) => point.id === targetId);
  const comparison = comparisons[targetId];

  targetVector.setAttribute("x2", target.x);
  targetVector.setAttribute("y2", target.y);
  targetVector.setAttribute(
    "class",
    `comparison-vector target ${comparison.className}${
      currentStep >= 4 ? " visible" : ""
    }`,
  );
  scoreElement.textContent = comparison.score;

  pairButtons.forEach((button) => {
    const active = button.dataset.target === targetId;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });

  pointElements.forEach((element, id) => {
    element.classList.toggle("selected", id === "cat" || id === targetId);
  });
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

  pointElements.forEach((element) => {
    element.classList.toggle("visible", currentStep >= 3);
  });
  baseVector.classList.toggle("visible", currentStep >= 4);
  targetVector.classList.toggle("visible", currentStep >= 4);
  renderComparison(selectedTarget);

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

pairButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    renderComparison(button.dataset.target);
  });
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

document.querySelector(".token-shell").addEventListener("click", (event) => {
  if (event.target.closest("button, a")) return;
  goTo(currentStep + 1);
});

window.addEventListener("popstate", () => {
  render(readStepFromUrl(), { updateHistory: false });
});

render(currentStep, { updateHistory: false });
