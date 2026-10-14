const TOTAL_STEPS = 5;

const steps = [
  {
    title: "A network starts with numbers.",
    copy: "Real-world information is translated into input values.",
    kicker: "Step 1 · Inputs",
    equation: "x = [0.9, 0.2, 0.7]",
    detail:
      "Each input represents a measurable feature. The network only sees numbers—not words, images, or meaning directly.",
  },
  {
    title: "Connections decide what matters.",
    copy: "Every connection carries a learned weight.",
    kicker: "Step 2 · Weights",
    equation:
      '<span class="accent">w₁</span>x₁ + <span class="accent">w₂</span>x₂ + <span class="accent">w₃</span>x₃',
    detail:
      "A large positive weight strengthens a signal. A small or negative weight weakens it.",
  },
  {
    title: "A neuron combines the signals.",
    copy: "The weighted sum passes through an activation function.",
    kicker: "Step 3 · Neuron",
    equation:
      'h = <span class="activation">activation</span>(w·x + b)',
    detail:
      "The bias shifts the threshold. The activation adds nonlinearity, letting the network model more than straight-line relationships.",
  },
  {
    title: "Layers build useful representations.",
    copy: "Outputs from one layer become inputs to the next.",
    kicker: "Step 4 · Forward pass",
    equation:
      'x → <span class="activation">hidden</span> → <span class="accent">ŷ</span>',
    detail:
      "Each layer recombines the previous layer’s signals. The final output is a prediction—in this example, a spam probability.",
  },
  {
    title: "Learning means tuning the connections.",
    copy: "Training changes the weights to make future predictions less wrong.",
    kicker: "Step 5 · Learning",
    equation:
      'error ↓ &nbsp; ⇒ &nbsp; weights <span class="activation">adjust</span>',
    detail:
      "The architecture stays in place. Learning repeatedly nudges millions or billions of weights toward better outputs.",
  },
];

const inputs = [
  { id: "x1", x: 105, y: 105, value: "0.9", name: "x₁" },
  { id: "x2", x: 105, y: 195, value: "0.2", name: "x₂" },
  { id: "x3", x: 105, y: 285, value: "0.7", name: "x₃" },
];

const hidden = [
  { id: "h1", x: 410, y: 72, value: "0.4", name: "h₁" },
  { id: "h2", x: 410, y: 154, value: "0.8", name: "h₂" },
  { id: "h3", x: 410, y: 236, value: "0.1", name: "h₃" },
  { id: "h4", x: 410, y: 318, value: "0.6", name: "h₄" },
];

const output = [{ id: "y", x: 710, y: 195, value: "87%", name: "spam" }];

const learnedInputWeights = [
  [4, 1.3, 2.8, 1.2],
  [1, 2.2, 1.1, 3.4],
  [3.4, 1.2, 2.3, 4],
];

const learnedOutputWeights = [1.1, 4, 0.8, 3.1];

const svgNamespace = "http://www.w3.org/2000/svg";
const connectionsGroup = document.querySelector("#connections");
const nodesGroup = document.querySelector("#nodes");
const titleElement = document.querySelector("#slide-title");
const copyElement = document.querySelector("#step-copy");
const kickerElement = document.querySelector("#concept-kicker");
const equationElement = document.querySelector("#equation");
const detailElement = document.querySelector("#concept-detail");
const previousButton = document.querySelector("#previous");
const nextButton = document.querySelector("#next");
const indicator = document.querySelector("#indicator");
const progressFill = document.querySelector("#progress-fill");

const nodeElements = new Map();
const connectionElements = [];

function createSvgElement(tag, attributes = {}) {
  const element = document.createElementNS(svgNamespace, tag);
  Object.entries(attributes).forEach(([key, value]) =>
    element.setAttribute(key, value),
  );
  return element;
}

function createNode(node, type) {
  const position = createSvgElement("g", {
    transform: `translate(${node.x} ${node.y})`,
  });
  const group = createSvgElement("g", {
    class: `node ${type}`,
    "data-node": node.id,
  });

  const circle = createSvgElement("circle", { r: type === "output" ? 44 : 34 });
  const value = createSvgElement("text", {
    class: "value",
    x: 0,
    y: type === "output" ? -4 : -3,
  });
  value.textContent = node.value;

  const name = createSvgElement("text", {
    class: "node-name",
    x: 0,
    y: type === "output" ? 17 : 15,
  });
  name.textContent = node.name;

  group.append(circle, value, name);
  position.appendChild(group);
  nodesGroup.appendChild(position);
  nodeElements.set(node.id, group);
}

function createConnection(from, to, phase, learnedWidth) {
  const line = createSvgElement("line", {
    class: "connection",
    x1: from.x + 35,
    y1: from.y,
    x2: to.x - (phase === "output" ? 45 : 35),
    y2: to.y,
    "data-phase": phase,
    "data-learned-width": learnedWidth,
  });

  connectionsGroup.appendChild(line);
  connectionElements.push(line);
}

inputs.forEach((input, inputIndex) => {
  hidden.forEach((neuron, hiddenIndex) => {
    createConnection(
      input,
      neuron,
      "input",
      learnedInputWeights[inputIndex][hiddenIndex],
    );
  });
});

hidden.forEach((neuron, index) => {
  createConnection(neuron, output[0], "output", learnedOutputWeights[index]);
});

inputs.forEach((node) => createNode(node, "input"));
hidden.forEach((node) => createNode(node, "hidden"));
output.forEach((node) => createNode(node, "output"));

function readStepFromUrl() {
  const value = Number(new URLSearchParams(window.location.search).get("step"));
  return Number.isInteger(value) && value >= 1 && value <= TOTAL_STEPS
    ? value
    : 1;
}

let currentStep = readStepFromUrl();

function setNodeVisibility(ids, visible) {
  ids.forEach((id) => nodeElements.get(id)?.classList.toggle("visible", visible));
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

  setNodeVisibility(
    inputs.map((node) => node.id),
    true,
  );
  setNodeVisibility(
    hidden.map((node) => node.id),
    currentStep >= 3,
  );
  setNodeVisibility(
    output.map((node) => node.id),
    currentStep >= 4,
  );

  hidden.forEach((node, index) => {
    nodeElements
      .get(node.id)
      ?.classList.toggle("active", currentStep >= 3 && index === 1);
  });
  nodeElements.get("y")?.classList.toggle("active", currentStep >= 4);

  connectionElements.forEach((line) => {
    const phase = line.dataset.phase;
    const isVisible =
      phase === "input" ? currentStep >= 2 : currentStep >= 4;
    line.classList.toggle("visible", isVisible);
    line.classList.toggle("learned", currentStep >= 5);
    line.style.strokeWidth =
      currentStep >= 5 ? line.dataset.learnedWidth : "1.6";
  });

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

document.querySelector(".visual-shell").addEventListener("click", (event) => {
  if (event.target.closest("button, a")) return;
  goTo(currentStep + 1);
});

window.addEventListener("popstate", () => {
  render(readStepFromUrl(), { updateHistory: false });
});

render(currentStep, { updateHistory: false });
