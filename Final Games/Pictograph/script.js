// Function to generate random numbers for questions
function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Game data: Levels with randomized questions and answers
const levels = [
  {
    level: 1,
    generateQuestion: () => {
      const bananasPerMonkey = getRandomNumber(2, 5);
      const mangoesPerParrot = getRandomNumber(2, 5);
      const monkeys = getRandomNumber(2, 5);
      const parrots = getRandomNumber(2, 5);
      return {
        pictograph: `🐒 + 🐒 = ${2 * bananasPerMonkey} 🍌\n🦜 + 🦜 + 🦜 = ${3 * mangoesPerParrot} 🥭`,
        question: `How many fruits (🍌 + 🥭) do ${monkeys} 🐒 and ${parrots} 🦜 have?`,
        answer: monkeys * bananasPerMonkey + parrots * mangoesPerParrot,
      };
    },
  },
  {
    level: 2,
    generateQuestion: () => {
      const fishPerGroup = getRandomNumber(2, 5);
      const octopusPerGroup = getRandomNumber(2, 5);
      const fish = getRandomNumber(2, 5);
      const octopus = getRandomNumber(2, 5);
      return {
        pictograph: `🐟 + 🐟 + 🐟 = ${3 * fishPerGroup} 🐠\n🐙 + 🐙 = ${2 * octopusPerGroup} 🦑`,
        question: `How many fishes (🐠 + 🦑) do ${fish} 🐟 and ${octopus} 🐙 have?`,
        answer: fish * fishPerGroup + octopus * octopusPerGroup,
      };
    },
  },
  {
    level: 3,
    generateQuestion: () => {
      const applesPerGroup = getRandomNumber(2, 5);
      const grapesPerGroup = getRandomNumber(2, 5);
      const apples = getRandomNumber(2, 5);
      const grapes = getRandomNumber(2, 5);
      return {
        pictograph: `🍎 + 🍎 = ${2 * applesPerGroup} 🍏\n🍇 + 🍇 + 🍇 = ${3 * grapesPerGroup} 🍓`,
        question: `How many fruits (🍏 + 🍓) do ${apples} 🍎 and ${grapes} 🍇 have?`,
        answer: apples * applesPerGroup + grapes * grapesPerGroup,
      };
    },
  },
];

// Shuffle and select 3 random questions
const selectedLevels = levels.sort(() => Math.random() - 0.5).slice(0, 3);

let currentLevel = 0;
let score = 0;
let currentQuestion;
let timeLeft = 300; // 5 minutes in seconds
let timerInterval;

// Function to load the current level
function loadLevel() {
  if (currentLevel >= selectedLevels.length) {
    endGame();
    return;
  }
  currentQuestion = selectedLevels[currentLevel].generateQuestion();
  document.getElementById("level-text").textContent = `Level ${currentLevel + 1}: Solve the puzzle!`;
  document.getElementById("pictograph").textContent = currentQuestion.pictograph;
  document.getElementById("question").textContent = currentQuestion.question;
  document.getElementById("answer").value = "";
  document.getElementById("result").textContent = "";
}

// Function to check the answer
function checkAnswer() {
  const userAnswer = parseInt(document.getElementById("answer").value);
  const resultElement = document.getElementById("result");
  if (userAnswer === currentQuestion.answer) {
    resultElement.textContent = "Correct! 🎉 You solved the puzzle!";
    resultElement.style.color = "green";
    document.getElementById("correct-sound").play();
    score += 10;
    document.getElementById("score").textContent = `Score: ${score}`;
  } else {
    resultElement.textContent = "Oops! Try again.";
    resultElement.style.color = "red";
    document.getElementById("wrong-sound").play();
  }
  currentLevel++;
  if (currentLevel < selectedLevels.length) {
    setTimeout(() => loadLevel(), 2000);
  } else {
    endGame();
  }
}

// Function to skip the current question
function skipQuestion() {
  currentLevel++;
  if (currentLevel < selectedLevels.length) {
    loadLevel();
  } else {
    endGame();
  }
}

// Function to update the timer
function updateTimer() {
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  document.getElementById("timer").textContent = `Time Left: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  if (timeLeft === 0) {
    endGame();
  } else {
    timeLeft--;
  }
}

// Function to end the game
function endGame() {
  clearInterval(timerInterval);
  document.getElementById("game-over-sound").play();
  setTimeout(() => {
    window.location.href = `results.html?score=${score}`;
  }, 2000);
}

timerInterval = setInterval(updateTimer, 1000);
loadLevel();
