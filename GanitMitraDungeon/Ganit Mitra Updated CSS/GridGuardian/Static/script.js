const challengeData = [
  { area: 6, perimeter: 10, hint: "Try 2×3 or 3×2 rectangle." },
  { area: 9, perimeter: 12, hint: "Try a 3×3 square." },
  { area: 8, perimeter: 12, hint: "Try 2×4 or 4×2 rectangle." },
  { area: 10, perimeter: 14, hint: "Try 2×5 or 5×2 rectangle." },
  { area: 12, perimeter: 16, hint: "Try 3×4 or 4×3 rectangle." }
];

const totalChallenges = challengeData.length;
let currentLevel = 1;
let score = 0;
let usedHint = false;
let gaveWrongAnswer = false;
let selectedCells = new Set();
let selectionOrder = 1; // ✅ Track the number order
let timerInterval;
let timeLeft = 150;

const gameGrid = document.getElementById("game-grid");
const requiredArea = document.getElementById("required-area");
const requiredPerimeter = document.getElementById("required-perimeter");
const currentArea = document.getElementById("current-area");
const currentPerimeter = document.getElementById("current-perimeter");
const feedback = document.getElementById("shape-feedback");
const scoreDisplay = document.getElementById("score-display");
const levelDisplay = document.getElementById("level-display");
const totalDisplay = document.getElementById("total-challenges");
const successModal = document.getElementById("success-modal");
const successMessage = document.getElementById("success-message");
const pointsEarned = document.getElementById("points-earned");
const hintModal = document.getElementById("hint-modal");
const hintText = document.getElementById("hint-text");
const timerDisplay = document.createElement("div");
const completeModal = document.getElementById("complete-modal");
const finalScoreDisplay = document.getElementById("final-score");

totalDisplay.textContent = totalChallenges;

// Create Grid
function createGrid(rows, cols) {
  gameGrid.innerHTML = "";
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.classList.add("grid-cell");
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.addEventListener("click", () => toggleCell(cell));
      gameGrid.appendChild(cell);
    }
  }
}

function toggleCell(cell) {
  const key = `${cell.dataset.row},${cell.dataset.col}`;
  if (selectedCells.has(key)) {
    selectedCells.delete(key);
    cell.classList.remove("selected");
    cell.textContent = "";
  } else {
    selectedCells.add(key);
    cell.classList.add("selected");
    cell.textContent = selectionOrder++; // ✅ show number in block
  }
  updateShapeStats();
}

function updateShapeStats() {
  const coords = Array.from(selectedCells).map(coord => {
    const [r, c] = coord.split(',').map(Number);
    return { r, c };
  });

  if (coords.length === 0) {
    currentArea.textContent = "0";
    currentPerimeter.textContent = "0";
    return;
  }

  let minRow = Math.min(...coords.map(p => p.r));
  let maxRow = Math.max(...coords.map(p => p.r));
  let minCol = Math.min(...coords.map(p => p.c));
  let maxCol = Math.max(...coords.map(p => p.c));

  const height = maxRow - minRow + 1;
  const width = maxCol - minCol + 1;
  const area = height * width;
  const perimeter = 2 * (height + width);

  currentArea.textContent = area;
  currentPerimeter.textContent = perimeter;
}

function clearShape() {
  selectedCells.forEach(key => {
    const [r, c] = key.split(",");
    const cell = document.querySelector(
      `.grid-cell[data-row="${r}"][data-col="${c}"]`
    );
    if (cell) {
      cell.classList.remove("selected");
      cell.textContent = "";
    }
  });
  selectedCells.clear();
  selectionOrder = 1; // ✅ reset order on clear
  updateShapeStats();
  feedback.textContent = "Select blocks on the grid to match the target!";
}

function loadChallenge(level) {
  const challenge = challengeData[level - 1];
  requiredArea.textContent = challenge.area;
  requiredPerimeter.textContent = challenge.perimeter;
  levelDisplay.textContent = level;
  clearShape();
  usedHint = false;
  gaveWrongAnswer = false;
  resetTimer();
  startTimer();
}

function submitShape() {
  const area = parseInt(currentArea.textContent);
  const perimeter = parseInt(currentPerimeter.textContent);
  const required = challengeData[currentLevel - 1];

  if (area === required.area && perimeter === required.perimeter) {
    clearInterval(timerInterval);

    // Final challenge completed
    if (currentLevel === totalChallenges) {
      let points = 0;
      if (!gaveWrongAnswer) {
        points = 100;
        if (usedHint) points -= 20;
        score += points;
      }
      finalScoreDisplay.textContent = score;
      completeModal.classList.remove("hidden");
      return;
    }

    if (gaveWrongAnswer) {
      successMessage.textContent = "✅ Correct, but no points due to earlier mistake.";
      pointsEarned.textContent = "0";
    } else {
      let points = 100;
      if (usedHint) points -= 20;
      score += points;
      pointsEarned.textContent = points;
      scoreDisplay.textContent = score;
      successMessage.textContent = `✅ Correct!${usedHint ? " (Hint used: -20 pts)" : ""}`;
    }

    successModal.classList.remove("hidden");
  } else {
    feedback.textContent = "❌ Incorrect! Try again.";
    gaveWrongAnswer = true;
  }
}

function nextChallenge() {
  currentLevel++;
  successModal.classList.add("hidden");
  loadChallenge(currentLevel);
}

function showHint() {
  hintText.textContent = challengeData[currentLevel - 1].hint;
  hintModal.classList.remove("hidden");
  usedHint = true;
}

function startTimer() {
  timeLeft = 100;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    timeLeft--;
    updateTimerDisplay();
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      gaveWrongAnswer = true;
      feedback.textContent = "⏰ Time's up! No points for this challenge.";
    }
  }, 1000);
}

function updateTimerDisplay() {
  timerDisplay.textContent = `⏳ Time Left: ${timeLeft}s`;
  timerDisplay.style.marginTop = "10px";
  timerDisplay.style.color = timeLeft < 20 ? "red" : "black";
  document.querySelector(".game-header").appendChild(timerDisplay);
}

function resetTimer() {
  clearInterval(timerInterval);
  timeLeft = 150;
  updateTimerDisplay();
}

// Event Listeners
document.getElementById("clear-btn").addEventListener("click", clearShape);
document.getElementById("submit-btn").addEventListener("click", submitShape);
document.getElementById("hint-btn").addEventListener("click", showHint);
document.getElementById("next-level-btn").addEventListener("click", nextChallenge);
document.getElementById("close-hint-btn").addEventListener("click", () => {
  hintModal.classList.add("hidden");
});

// Init
createGrid(10, 10);
loadChallenge(currentLevel);
