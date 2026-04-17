const classMeta = {
  benign: {
    title: 'Benign',
    detail: 'The URL looks safe relative to the model features it has seen.',
    tone: 'benign',
  },
  defacement: {
    title: 'Defacement',
    detail: 'The URL has signals that often appear in site tampering attempts.',
    tone: 'defacement',
  },
  malware: {
    title: 'Malware',
    detail: 'The lexical pattern resembles malicious download or payload delivery paths.',
    tone: 'malware',
  },
  phishing: {
    title: 'Phishing',
    detail: 'The URL shows suspicious account or verification wording and related traits.',
    tone: 'phishing',
  },
};

const classLabels = ['benign', 'defacement', 'malware', 'phishing'];

const confusionMatrix = [
  [4084, 12, 22, 87],
  [22, 1097, 94, 182],
  [35, 77, 5560, 371],
  [155, 111, 238, 6676],
];

const evaluationSummary = {
  business: '2 pass, 1 partial',
  technical: 'Accuracy target met',
  assessment:
    'The tuned Random Forest is suitable for deployment with minor limitations, which is why the frontend promotes it as the active production model.',
};

const state = {
  total: confusionMatrix.flat().reduce((sum, value) => sum + value, 0),
  correct: confusionMatrix.reduce((sum, row, index) => sum + row[index], 0),
};

const elements = {
  form: document.getElementById('predictionForm'),
  input: document.getElementById('urlInput'),
  badge: document.getElementById('predictionBadge'),
  message: document.getElementById('predictionMessage'),
  matrix: document.getElementById('confusionMatrix'),
  errorProfile: document.getElementById('errorProfile'),
};

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function renderMatrix() {
  const maxValue = Math.max(...confusionMatrix.flat());
  const headerRow = [
    '<div class="matrix-label corner">Actual \ Predicted</div>',
    ...classLabels.map((label) => `<div class="matrix-label">${label}</div>`),
  ].join('');

  const rows = confusionMatrix
    .map((row, rowIndex) => {
      const cells = row
        .map((value, colIndex) => {
          const intensity = 0.08 + (value / maxValue) * 0.86;
          const isDiagonal = rowIndex === colIndex;
          const color = isDiagonal ? '47, 212, 176' : '242, 177, 52';
          return `
            <div class="matrix-cell" style="background: rgba(${color}, ${intensity});">
              <small>${classLabels[rowIndex]} → ${classLabels[colIndex]}</small>
              <span>${value.toLocaleString()}</span>
            </div>
          `;
        })
        .join('');

      return `<div class="matrix-label">${classLabels[rowIndex]}</div>${cells}`;
    })
    .join('');

  elements.matrix.innerHTML = `${headerRow}${rows}`;
}

function renderErrorProfile() {
  const total = state.total;

  const rows = confusionMatrix.map((row, index) => {
    const support = row.reduce((sum, value) => sum + value, 0);
    const correct = row[index];
    const errors = support - correct;
    const errorRate = errors / support;
    const supportShare = support / total;
    const width = Math.max(errorRate, 0.04) * 100;

    return `
      <div class="bar-row">
        <div class="bar-topline">
          <span>${classLabels[index]}</span>
          <span>${errors.toLocaleString()} errors · ${formatPercent(errorRate)} miss rate</span>
        </div>
        <div class="bar-track" aria-hidden="true">
          <div class="bar-fill" style="width: ${width}%;"></div>
        </div>
        <div class="bar-topline" style="margin-top: 0.65rem; margin-bottom: 0; color: var(--muted);">
          <span>Support ${support.toLocaleString()}</span>
          <span>${formatPercent(supportShare)} of evaluation set</span>
        </div>
      </div>
    `;
  });

  elements.errorProfile.innerHTML = rows.join('');
}

function updateResult(label) {
  const meta = classMeta[label] || {
    title: label,
    detail: 'The model returned an unexpected class label.',
    tone: 'neutral',
  };

  elements.badge.className = `prediction-badge ${meta.tone}`;
  elements.badge.textContent = meta.title;
  elements.message.textContent = meta.detail;
}

async function submitPrediction(event) {
  event.preventDefault();
  const url = elements.input.value.trim();

  if (!url) {
    updateResult('neutral');
    elements.message.textContent = 'Enter a URL to classify it.';
    return;
  }

  elements.badge.className = 'prediction-badge neutral';
  elements.badge.textContent = 'Classifying...';
  elements.message.textContent = 'Running feature extraction and model inference.';
  elements.form.querySelector('button').disabled = true;

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`Prediction request failed with status ${response.status}`);
    }

    const payload = await response.json();
    updateResult(payload.prediction);
  } catch (error) {
    elements.badge.className = 'prediction-badge neutral';
    elements.badge.textContent = 'Error';
    elements.message.textContent = 'The API request failed. Make sure the FastAPI server is running.';
  } finally {
    elements.form.querySelector('button').disabled = false;
  }
}

function bindSampleChips() {
  document.querySelectorAll('.sample-chip').forEach((button) => {
    button.addEventListener('click', () => {
      elements.input.value = button.dataset.url || '';
      elements.input.focus();
    });
  });
}

function hydrateSummary() {
  const summaryCards = document.querySelectorAll('.summary-card');
  if (summaryCards.length < 3) {
    return;
  }

  summaryCards[0].querySelector('strong').textContent = evaluationSummary.business;
  summaryCards[1].querySelector('strong').textContent = evaluationSummary.technical;
  summaryCards[2].querySelector('p').textContent = evaluationSummary.assessment;
}

renderMatrix();
renderErrorProfile();
bindSampleChips();
hydrateSummary();
elements.form.addEventListener('submit', submitPrediction);
updateResult('neutral');