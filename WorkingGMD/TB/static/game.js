// Game state
let gameState = 'start';
let gameMode = 'even';
let score = 0;
let combo = 0;
let highestCombo = 0;
let timeLeft = 60;
let difficulty = 1;
let targets = [];
let targetIdCounter = 0;
let highScore = parseInt(localStorage.getItem('ninjaHighScore') || '0');


function isPrime(num) {
  if (num < 2) return false;
  for (let i = 2; i <= Math.sqrt(num); i++) {
    if (num % i === 0) return false;
  }
  return true;
}

function startGame(mode) {
  gameMode = mode;
  gameState = 'playing';
  score = 0;
  combo = 0;
  highestCombo = 0;
  timeLeft = 60;
  difficulty = 1;
  targets = [];

  document.getElementById('startScreen').classList.add('hidden');
  document.getElementById('gameScreen').classList.remove('hidden');
  document.getElementById('modeDisplay').textContent = `Mode: ${mode.toUpperCase()}`;
  document.getElementById('scoreValue').textContent = '0';
  document.getElementById('comboDisplay').classList.add('hidden');

  startGameLoop();
}

function endGame() {
  gameState = 'gameOver';
  if (score > highScore) {
    highScore = score;
    localStorage.setItem('ninjaHighScore', highScore.toString());
    document.getElementById('newHighScore').classList.remove('hidden');
  }

  document.getElementById('gameScreen').classList.add('hidden');
  document.getElementById('gameOverScreen').classList.remove('hidden');
  document.getElementById('finalScoreValue').textContent = score;
  document.getElementById('finalHighScore').textContent = highScore;
  document.getElementById('targetsHit').textContent = Math.floor(score / 10);
  document.getElementById('highestCombo').textContent = highestCombo;

  playSound('gameOver');
}

function restartGame() {
  gameState = 'start';
  document.getElementById('gameOverScreen').classList.add('hidden');
  document.getElementById('startScreen').classList.remove('hidden');
  document.getElementById('newHighScore').classList.add('hidden');
  updateHighScoreDisplay();
}

function generateTarget() {
  const gameArea = document.getElementById('gameArea');
  const { width, height } = gameArea.getBoundingClientRect();

  const size = Math.floor(40 + Math.random() * 30);
  const x = Math.floor(size + Math.random() * (width - size * 2));
  const y = Math.floor(size + Math.random() * (height - size * 2));
  const speed = 1 + Math.random() * difficulty;

  let value;
  const isCorrect = Math.random() < 0.7;

  if (gameMode === 'even') {
    value = isCorrect ? 2 * Math.floor(Math.random() * 49) + 2 : 2 * Math.floor(Math.random() * 49) + 1;
  } else if (gameMode === 'odd') {
    value = isCorrect ? 2 * Math.floor(Math.random() * 49) + 1 : 2 * Math.floor(Math.random() * 49) + 2;
  } else if (gameMode === 'prime') {
    const primes = Array.from({ length: 50 }, (_, i) => i + 2).filter(isPrime);
    const nonPrimes = Array.from({ length: 98 }, (_, i) => i + 2).filter(n => !isPrime(n));
    const list = isCorrect ? primes : nonPrimes;
    value = list[Math.floor(Math.random() * list.length)];
  }


  const target = {
    id: targetIdCounter++,
    value,
    x,
    y,
    size,
    speed,
    direction: {
      x: Math.random() > 0.5 ? 1 : -1,
      y: Math.random() > 0.5 ? 1 : -1
    }
  };

  targets.push(target);
  createTargetElement(target);
}

function createTargetElement(target) {
  const el = document.createElement('div');
  el.className = 'number-target';
  el.id = `target-${target.id}`;
  el.textContent = target.value;

  const correct =
    (gameMode === 'even' && target.value % 2 === 0) ||
    (gameMode === 'odd' && target.value % 2 !== 0) ||
    (gameMode === 'prime' && isPrime(target.value));

  el.style.backgroundColor = correct ? 'var(--target-correct-bg)' : 'var(--target-wrong-bg)';
  el.style.color = correct ? 'var(--target-correct-text)' : 'var(--target-wrong-text)';
  el.style.width = `${target.size}px`;
  el.style.height = `${target.size}px`;
  el.style.fontSize = `${target.size / 2}px`;
  el.style.left = `${target.x}px`;
  el.style.top = `${target.y}px`;

  el.onclick = () => handleTargetClick(target);
  document.getElementById('gameArea').appendChild(el);
}

function handleTargetClick(target) {
  const correct =
    (gameMode === 'even' && target.value % 2 === 0) ||
    (gameMode === 'odd' && target.value % 2 !== 0) ||
    (gameMode === 'prime' && isPrime(target.value));

  removeTarget(target);

  if (correct) {
    const points = Math.floor(10 * (1 + combo * 0.1));
    score += points;
    combo++;
    highestCombo = Math.max(highestCombo, combo);
    document.getElementById('scoreValue').textContent = score;
    document.getElementById('comboDisplay').classList.remove('hidden');
    document.getElementById('comboValue').textContent = `x${combo}`;
    
    createSliceEffect(target.x, target.y);
    createBurstEffect(target.x, target.y);
  } else {
    combo = 0;
    document.getElementById('comboDisplay').classList.add('hidden');
    
  }
}

function removeTarget(target) {
  const index = targets.findIndex(t => t.id === target.id);
  if (index !== -1) {
    targets.splice(index, 1);
    const el = document.getElementById(`target-${target.id}`);
    if (el) el.remove();
  }
}

function createSliceEffect(x, y) {
  const effect = document.createElement('div');
  effect.className = 'slice-effect';
  effect.style.left = `${x}px`;
  effect.style.top = `${y}px`;
  document.getElementById('gameArea').appendChild(effect);
  setTimeout(() => effect.remove(), 500);
}

function createBurstEffect(x, y) {
  const burst = document.createElement('div');
  burst.className = 'bubble-burst';
  burst.style.left = `${x}px`;
  burst.style.top = `${y}px`;
  document.getElementById('gameArea').appendChild(burst);
  setTimeout(() => burst.remove(), 400);
}

function updateTargets() {
  targets.forEach(target => {
    const el = document.getElementById(`target-${target.id}`);
    if (!el) return;

    const gameArea = document.getElementById('gameArea');
    const { width, height } = gameArea.getBoundingClientRect();

    target.x += target.direction.x * target.speed;
    target.y += target.direction.y * target.speed;

    if (target.x <= target.size / 2 || target.x >= width - target.size / 2) {
      target.direction.x *= -1;
    }
    if (target.y <= target.size / 2 || target.y >= height - target.size / 2) {
      target.direction.y *= -1;
    }

    el.style.left = `${target.x}px`;
    el.style.top = `${target.y}px`;
  });
}

function updateTimer() {
  timeLeft--;
  document.getElementById('timerValue').textContent = timeLeft;
  document.getElementById('timerBar').style.width = `${(timeLeft / 60) * 100}%`;

  if (timeLeft <= 10) {
    document.querySelector('.timer').classList.add('timer-warning');
  }

  if (timeLeft <= 0) {
    endGame();
  }
}

let gameLoop, targetGenerator, difficultyIncreaser;

function startGameLoop() {
  clearInterval(gameLoop);
  clearInterval(targetGenerator);
  clearInterval(difficultyIncreaser);

  gameLoop = setInterval(() => {
    if (gameState === 'playing') updateTargets();
  }, 30);

  targetGenerator = setInterval(() => {
    if (gameState === 'playing' && targets.length < Math.floor(5 + difficulty * 2)) {
      generateTarget();
    }
  }, Math.max(200, 1000 - difficulty * 100));

  const timer = setInterval(() => {
    if (gameState === 'playing') updateTimer();
    else clearInterval(timer);
  }, 1000);

  difficultyIncreaser = setInterval(() => {
    if (gameState === 'playing') {
      difficulty = Math.min(difficulty + 0.5, 10);
    }
  }, 10000);
}


function goBackToMenu() {
  gameState = 'start';
  document.getElementById("gameScreen").classList.add("hidden");
  document.getElementById("startScreen").classList.remove("hidden");
  document.getElementById("gameOverScreen").classList.add("hidden");

  clearInterval(gameLoop);
  clearInterval(targetGenerator);
  clearInterval(difficultyIncreaser);

  targets.forEach(target => {
    const el = document.getElementById(`target-${target.id}`);
    if (el) el.remove();
  });
  targets = [];

  document.getElementById('comboDisplay').classList.add('hidden');
  document.getElementById('timerValue').textContent = '60';
  document.getElementById('timerBar').style.width = '100%';
  document.querySelector('.timer').classList.remove('timer-warning');

  updateHighScoreDisplay();
}

// Show high score on start
function updateHighScoreDisplay() {
  const displayElement = document.getElementById("highScoreDisplay");
  if (displayElement) {
    displayElement.textContent = localStorage.getItem("ninjaHighScore") || 0;
  }
}

window.onload = () => {
  updateHighScoreDisplay();
};
