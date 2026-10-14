const TOTAL_STEPS = 8;

const steps = [
  {
    title: "Training starts with ordinary text.",
    copy: "Documents are collected, cleaned, tokenized, and packed into sequences.",
    kicker: "Step 1 · Data",
    equation:
      'text → <span class="data-color">token sequences</span>',
    detail:
      "Pretraining data can include books, articles, code, reference material, and other text. Quality, diversity, duplication, and licensing all matter.",
  },
  {
    title: "The text supplies its own labels.",
    copy: "At every position, the next token becomes the correct target.",
    kicker: "Step 2 · Targets",
    equation:
      '[x₁, x₂, x₃] → <span class="learn-color">[x₂, x₃, x₄]</span>',
    detail:
      "This is self-supervised learning: no person needs to label each example. Shifting the sequence by one creates billions of prediction targets.",
  },
  {
    title: "The model makes a prediction.",
    copy: "A forward pass produces a probability distribution for the next token.",
    kicker: "Step 3 · Forward pass",
    equation:
      'context → model → <span class="data-color">P(next token)</span>',
    detail:
      "The current weights determine the prediction. Early in training, the correct token may receive little probability.",
  },
  {
    title: "Loss measures how wrong the prediction was.",
    copy: "Cross-entropy penalizes low probability on the correct target.",
    kicker: "Step 4 · Loss",
    equation:
      '<span class="loss-color">L</span> = −log P(correct token)',
    detail:
      "A confident correct prediction has low loss. A confident wrong prediction has high loss. Training minimizes the average loss across a batch.",
  },
  {
    title: "Backpropagation assigns responsibility.",
    copy: "Gradients measure how each parameter contributed to the loss.",
    kicker: "Step 5 · Backprop",
    equation:
      '<span class="loss-color">∂L/∂w</span> for every weight',
    detail:
      "Automatic differentiation works backward through the computation graph, producing a gradient for every trainable parameter.",
  },
  {
    title: "The optimizer nudges the weights.",
    copy: "A small update should make the correct token more likely next time.",
    kicker: "Step 6 · Update",
    equation:
      'w ← w − <span class="learn-color">learning_rate × gradient</span>',
    detail:
      "Optimizers such as Adam combine gradients with running statistics. Click the update button to watch loss fall on this simplified example.",
  },
  {
    title: "Learning is the loop repeated at scale.",
    copy: "Batches flow through the model for millions of optimization steps.",
    kicker: "Step 7 · Scale",
    equation:
      'predict → measure → update → <span class="learn-color">repeat</span>',
    detail:
      "Real training distributes huge batches across many accelerators. The loss curve is noisy, but its long-term trend should move downward.",
  },
  {
    title: "Different training phases shape different capabilities.",
    copy: "Pretraining builds the model; post-training makes it more useful and aligned.",
    kicker: "Step 8 · Training phases",
    equation:
      'pretrain → instruct → <span class="learn-color">align</span>',
    detail:
      "These phases use different datasets and objectives. Explore each phase to see what changes—and what it is intended to teach.",
  },
];

const phaseContent = {
  pretraining: {
    data: "massive unlabeled text corpora",
    objective: "minimize next-token loss",
    result: "general language and world patterns",
  },
  instruction: {
    data: "prompt-and-response demonstrations",
    objective: "imitate helpful target answers",
    result: "instruction following and task behavior",
  },
  preference: {
    data: "ranked or compared model responses",
    objective: "increase preference-aligned behavior",
    result: "more helpful, safe, and consistent responses",
  },
};

const probabilityStates = [
  { rug: 0.42, mat: 0.18, floor: 0.16, bed: 0.12 },
  { rug: 0.34, mat: 0.29, floor: 0.15, bed: 0.11 },
  { rug: 0.27, mat: 0.41, floor: 0.13, bed: 0.09 },
  { rug: 0.2, mat: 0.55, floor: 0.1, bed: 0.07 },
  { rug: 0.14, mat: 0.68, floor: 0.07, bed: 0.05 },
];

const lossStates = probabilityStates.map((state) => -Math.log(state.mat));
const titleElement = document.querySelector("#slide-title");
const copyElement = document.querySelector("#step-copy");
const kickerElement = document.querySelector("#concept-kicker");
const equationElement = document.querySelector("#equation");
const detailElement = document.querySelector("#concept-detail");
const previousButton = document.querySelector("#previous");
const nextButton = document.querySelector("#next");
const indicator = document.querySelector("#indicator");
const progressFill = document.querySelector("#progress-fill");
const miniDistribution = document.querySelector("#mini-distribution");
const lossValue = document.querySelector("#loss-value");
const weightValue = document.querySelector("#weight-value");
const modelBox = document.querySelector("#model-box");
const stepCount = document.querySelector("#step-count");
const lossCurve = document.querySelector("#loss-curve");
const lossPoints = document.querySelector("#loss-points");
const updateButton = document.querySelector("#update-button");
const phaseButtons = [...document.querySelectorAll(".phase-card")];
const phaseData = document.querySelector("#phase-data");
const phaseObjective = document.querySelector("#phase-objective");
const phaseResult = document.querySelector("#phase-result");
let trainingUpdate = 0;

Object.keys(probabilityStates[0]).forEach((token) => {
  const row = document.createElement("div");
  row.className = `mini-candidate${token === "mat" ? " target" : ""}`;
  row.dataset.token = token;
  row.innerHTML =
    `<span>${token}</span>` +
    `<i></i>` +
    `<span class="probability"></span>`;
  miniDistribution.appendChild(row);
});

function readStepFromUrl() {
  const value = Number(new URLSearchParams(window.location.search).get("step"));
  return Number.isInteger(value) && value >= 1 && value <= TOTAL_STEPS
    ? value
    : 1;
}

let currentStep = readStepFromUrl();

function renderProbabilities() {
  const probabilities = probabilityStates[trainingUpdate];
  Object.entries(probabilities).forEach(([token, probability]) => {
    const row = miniDistribution.querySelector(`[data-token="${token}"]`);
    row.querySelector("i").style.width = `${probability * 100}%`;
    row.querySelector(".probability").textContent =
      `${Math.round(probability * 100)}%`;
  });
  lossValue.textContent = lossStates[trainingUpdate].toFixed(2);
  weightValue.textContent = `w = ${(0.18 + trainingUpdate * 0.11).toFixed(2)}`;
  stepCount.textContent = `step ${trainingUpdate}`;
  modelBox.classList.toggle("updated", trainingUpdate > 0);
  renderLossCurve();
}

function renderLossCurve() {
  const shownLosses = lossStates.slice(0, trainingUpdate + 1);
  const points = shownLosses.map((loss, index) => {
    const x = 22 + index * 75;
    const y = 15 + (loss / lossStates[0]) * 52;
    return { x, y };
  });
  lossCurve.setAttribute(
    "d",
    points.map((point, index) =>
      `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`,
    ).join(" "),
  );
  lossPoints.innerHTML = "";
  points.forEach((point) => {
    const circle = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "circle",
    );
    circle.setAttribute("cx", point.x);
    circle.setAttribute("cy", point.y);
    circle.setAttribute("r", 3.5);
    lossPoints.appendChild(circle);
  });
}

function runUpdate() {
  trainingUpdate = Math.min(
    probabilityStates.length - 1,
    trainingUpdate + 1,
  );
  renderProbabilities();
  updateButton.textContent =
    trainingUpdate === probabilityStates.length - 1
      ? "Example converged"
      : "Run optimizer step";
  updateButton.disabled =
    trainingUpdate === probabilityStates.length - 1;
}

function renderPhase(phaseName) {
  const content = phaseContent[phaseName];
  phaseButtons.forEach((button) => {
    const active = button.dataset.phase === phaseName;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  phaseData.textContent = content.data;
  phaseObjective.textContent = content.objective;
  phaseResult.textContent = content.result;
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

  if (currentStep === 7 && trainingUpdate < probabilityStates.length - 1) {
    trainingUpdate = probabilityStates.length - 1;
  }
  renderProbabilities();

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

updateButton.addEventListener("click", (event) => {
  event.stopPropagation();
  runUpdate();
});

phaseButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    renderPhase(button.dataset.phase);
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

document.querySelector(".training-shell").addEventListener("click", (event) => {
  if (event.target.closest("button, a")) return;
  goTo(currentStep + 1);
});

window.addEventListener("popstate", () => {
  render(readStepFromUrl(), { updateHistory: false });
});

renderPhase("pretraining");
render(currentStep, { updateHistory: false });
