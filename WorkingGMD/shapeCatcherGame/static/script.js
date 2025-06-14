 // Game variables
 let currentQuestion = {};
 let correctAnswer = 0;
 let score = 0;
 let timeLeft = 30;
 let gameInterval;
 let shapeInterval;
 let gameActive = false;
 let shapeDropRate = 600; // Faster initial shape drop rate (ms)
 let shapeSpeed = 4; // Faster initial falling speed
 let currentLevel = 1;
 let questionsAnswered = 0;
 let bestScores = {}; // To store best scores for each question

 // Shape images (using emoji for simplicity)
 const shapeImages = {
     3: '🔺', // Triangle
     4: '🟦', // Square
     5: '⬟', // Pentagon
     6: '⬢', // Hexagon
     7: '🟣', // Circle (for 7+)
     8: '⭐', // Star (for 8+)
     9: '🟧', // Nonagon (represented by square)
     10: '🔳' // Decagon (represented by square)
 };

 const shapeNames = {
     3: 'Triangles',
     4: 'Squares',
     5: 'Pentagons',
     6: 'Hexagons',
     7: 'Circles',
     8: 'Stars',
     9: 'Nonagons',
     10: 'Decagons'
 };

 // Fraction questions database for class 5 with explanations
 const questions = [
     // Level 1 - Basic fraction identification
     {
         question: "What fraction of the shape is colored? (1 out of 4 parts colored)",
         answers: ["1/2", "1/3", "1/4", "1/5"],
         correct: "1/4",
         explanation: "When 1 part out of 4 equal parts is colored, the fraction is 1/4."
     }, {
         question: "Which fraction represents 'three quarters'?",
         answers: ["2/4", "3/4", "4/3", "1/4"],
         correct: "3/4",
         explanation: "Three quarters means 3 parts out of 4, which is written as 3/4."
     }, {
         question: "What is the numerator in the fraction 2/5?",
         answers: ["2", "5", "7", "3"],
         correct: "2",
         explanation: "In a fraction, the top number is called the numerator."
     }, {
         question: "Which shape shows the fraction 1/2? (Half colored)",
         answers: ["Circle half colored", "Square with 1/4 colored", "Triangle with 1/3 colored", "Rectangle with 3/4 colored"],
         correct: "Circle half colored",
         explanation: "1/2 means half of the shape should be colored."
     },

     // Level 2 - Equivalent fractions
     {
         question: "Which fraction is equivalent to 1/2?",
         answers: ["2/4", "1/3", "3/5", "2/3"],
         correct: "2/4",
         explanation: "2/4 simplifies to 1/2 when you divide both numerator and denominator by 2."
     }, {
         question: "What is the simplest form of 4/8?",
         answers: ["1/2", "2/4", "4/8", "1/4"],
         correct: "1/2",
         explanation: "Divide both numerator and denominator by 4 to simplify 4/8 to 1/2."
     }, {
         question: "Which fraction is NOT equivalent to the others?",
         answers: ["1/2", "2/4", "3/6", "2/3"],
         correct: "2/3",
         explanation: "1/2, 2/4 and 3/6 all equal 1/2 when simplified, but 2/3 is different."
     }, {
         question: "Complete the equivalent fraction: 2/3 = ?/6",
         answers: ["3", "4", "5", "6"],
         correct: "4",
         explanation: "Multiply numerator and denominator by 2: 2×2=4 and 3×2=6, so 2/3 = 4/6."
     },

     // Level 3 - Fraction comparison and ordering
     {
         question: "Which fraction is larger: 1/3 or 1/4?",
         answers: ["1/3", "1/4", "They're equal", "Can't compare"],
         correct: "1/3",
         explanation: "When numerators are the same, the fraction with the smaller denominator is larger."
     }, {
         question: "Arrange these fractions from smallest to largest: 1/2, 1/4, 1/8",
         answers: ["1/8, 1/4, 1/2", "1/2, 1/4, 1/8", "1/4, 1/8, 1/2", "They're equal"],
         correct: "1/8, 1/4, 1/2",
         explanation: "With the same numerator, smaller denominators mean larger fractions."
     }, {
         question: "Which fraction is closest to 1: 3/4, 5/6, or 7/8?",
         answers: ["3/4", "5/6", "7/8", "They're equal"],
         correct: "7/8",
         explanation: "7/8 is only 1/8 away from 1, which is closer than the others."
     }, {
         question: "Which symbol goes between these fractions: 2/3 _ 3/4?",
         answers: [">", "<", "=", "≥"],
         correct: "<",
         explanation: "2/3 ≈ 0.666 and 3/4 = 0.75, so 2/3 is less than 3/4."
     },

     // Level 4 - Fraction addition and subtraction
     {
         question: "What is 1/4 + 1/4?",
         answers: ["1/2", "2/4", "1/8", "2/8"],
         correct: "1/2",
         explanation: "When denominators are the same, add numerators: 1+1=2, so 2/4 which simplifies to 1/2."
     }, {
         question: "Calculate: 3/5 - 1/5",
         answers: ["2/5", "1/5", "4/5", "2/10"],
         correct: "2/5",
         explanation: "With same denominators, subtract numerators: 3-1=2, so 2/5."
     }, {
         question: "What is 1/2 + 1/3? (Find common denominator first)",
         answers: ["2/5", "3/6", "5/6", "2/6"],
         correct: "5/6",
         explanation: "Convert to common denominator 6: 3/6 + 2/6 = 5/6."
     }, {
         question: "If you eat 1/8 of a pizza and then eat another 3/8, how much did you eat total?",
         answers: ["1/2", "4/8", "4/16", "Both A and B"],
         correct: "Both A and B",
         explanation: "1/8 + 3/8 = 4/8 which simplifies to 1/2."
     }
 ];

 // DOM elements
 const homeScreen = document.getElementById('home-screen');
 const menuPage = document.getElementById('menu-page');
 const gamePage = document.getElementById('game-page');
 const gameOverPage = document.getElementById('game-over-page');
 const questionText = document.getElementById('question-text');
 const answerButtons = document.querySelectorAll('.answer-btn');
 const feedbackMessage = document.getElementById('feedback-message');
 const explanationDisplay = document.getElementById('explanation');
 const startGameBtn = document.getElementById('start-game-btn');
 const scoreDisplay = document.getElementById('score-display');
 const timeDisplay = document.getElementById('time-display');
 const levelDisplay = document.getElementById('level-display');
 const gameArea = document.getElementById('game-area');
 const catcher = document.getElementById('catcher');
 const targetShapeDisplay = document.getElementById('target-shape-display');
 const finalScoreDisplay = document.getElementById('final-score');
 const starsDisplay = document.querySelectorAll('#stars .star');
 const targetShapeResult = document.getElementById('target-shape-result');
 const shapeNameDisplay = document.getElementById('shape-name');
 const bestScoresList = document.getElementById('best-scores-list');
 const playAgainBtn = document.getElementById('play-again-btn');
 const nextQuestionBtn = document.getElementById('next-question-btn');
 const homeBtn = document.getElementById('home-btn');
 const startBtn = document.getElementById('start-btn');
 const quitBtn = document.getElementById('quit-btn');

 // Initialize the game
 function initGame() {
     loadRandomQuestion();
     setupEventListeners();
 }

 // Load a random question based on current level
 function loadRandomQuestion() {
     // Filter questions by level (each level has 4 questions)
     const levelStart = (currentLevel - 1) * 4;
     const levelEnd = levelStart + 4;
     const levelQuestions = questions.slice(levelStart, levelEnd);

     // If we've answered all questions in this level, move to next level
     if (questionsAnswered >= 4) {
         currentLevel++;
         questionsAnswered = 0;
         if (currentLevel > 4) {
             // If all levels completed, start from beginning
             currentLevel = 1;
         }
     }

     // Get a random question from current level
     const randomIndex = Math.floor(Math.random() * levelQuestions.length);
     currentQuestion = levelQuestions[randomIndex];
     correctAnswer = currentQuestion.correct;

     questionText.textContent = currentQuestion.question;

     // Set answer buttons
     answerButtons.forEach((btn, index) => {
         btn.textContent = currentQuestion.answers[index];
         btn.dataset.answer = currentQuestion.answers[index];
     });

     // Reset UI
     feedbackMessage.textContent = '';
     explanationDisplay.textContent = '';
     explanationDisplay.style.display = 'none';
     startGameBtn.style.display = 'none';

     // Update level display
     levelDisplay.textContent = `Level: ${currentLevel}`;
 }

 // Set up event listeners
 function setupEventListeners() {
     // Home screen buttons
     startBtn.addEventListener('click', showMenuPage);
     quitBtn.addEventListener('click', () => {
         alert('Thanks for playing! Come back soon!');
         // In a real app, you might close the window or redirect
     });

     // Answer buttons
     answerButtons.forEach(btn => {
         btn.addEventListener('click', checkAnswer);
     });

     // Start game button
     startGameBtn.addEventListener('click', startGame);

     // Game over buttons
     playAgainBtn.addEventListener('click', playAgain);
     nextQuestionBtn.addEventListener('click', nextQuestion);
     homeBtn.addEventListener('click', showHomeScreen);

     // Mouse movement controls
     gameArea.addEventListener('mousemove', moveCatcherMouse);
     gameArea.addEventListener('touchmove', moveCatcherTouch, {
         passive: false
     });
 }

 // Show menu page
 function showMenuPage() {
     homeScreen.style.display = 'none';
     menuPage.style.display = 'flex';
     gamePage.style.display = 'none';
     gameOverPage.style.display = 'none';
 }

 // Show home screen
 function showHomeScreen() {
     homeScreen.style.display = 'flex';
     menuPage.style.display = 'none';
     gamePage.style.display = 'none';
     gameOverPage.style.display = 'none';
 }

 // Check the selected answer
 function checkAnswer(e) {
     const selectedAnswer = e.target.dataset.answer;

     // Show explanation regardless of answer
     if (currentQuestion.explanation) {
         explanationDisplay.textContent = currentQuestion.explanation;
         explanationDisplay.style.display = 'block';
     }

     if (selectedAnswer === correctAnswer.toString()) {
         handleCorrectAnswer();
     } else {
         handleWrongAnswer();
     }
 }

 function handleCorrectAnswer() {
     feedbackMessage.textContent = 'Correct! 🎉';
     feedbackMessage.style.color = '#4CAF50';
     startGameBtn.style.display = 'block';
     playSound('correct');
     questionsAnswered++;

     // Add celebration effect
     celebrate();

     // Update best score for this question if needed
     const questionKey = currentQuestion.question.substring(0, 30);
     if (!bestScores[questionKey] || score > bestScores[questionKey]) {
         bestScores[questionKey] = score;
     }
 }

 function handleWrongAnswer() {
     feedbackMessage.textContent = 'Oops! Try again.';
     feedbackMessage.style.color = '#d32f2f';
     playSound('wrong');
 }

 // Start the shape catching game
 function startGame() {
     menuPage.style.display = 'none';
     gamePage.style.display = 'flex';
     gameOverPage.style.display = 'none';

     // Reset game variables
     score = 0;
     timeLeft = 30;
     gameActive = true;
     shapeDropRate = 600 - (currentLevel * 100); // Faster drop rate based on level
     shapeSpeed = 4 + currentLevel; // Faster speed based on level

     // Update displays
     scoreDisplay.textContent = `Score: ${score}`;
     timeDisplay.textContent = `Time: ${timeLeft}`;
     levelDisplay.textContent = `Level: ${currentLevel}`;

     // Set target shape
     let shapeKey;
     if (typeof correctAnswer === 'number') {
         shapeKey = correctAnswer > 10 ? 10 : correctAnswer < 3 ? 3 : correctAnswer;
     } else {
         // For non-number answers, use length of correct answer string
         shapeKey = correctAnswer.length > 10 ? 10 : correctAnswer.length < 3 ? 3 : correctAnswer.length;
     }

     targetShapeDisplay.textContent = shapeImages[shapeKey];
     targetShapeDisplay.style.fontSize = '50px';

     // Start game timer
     gameInterval = setInterval(updateGame, 1000);

     // Start creating falling shapes (more frequently)
     shapeInterval = setInterval(createFallingShape, shapeDropRate);

     playSound('game-start');
 }

 // Update game state
 function updateGame() {
     timeLeft--;
     timeDisplay.textContent = `Time: ${timeLeft}`;

     // Increase difficulty as time passes
     if (timeLeft % 5 === 0 && shapeDropRate > 300) {
         shapeDropRate -= 50;
         shapeSpeed += 0.5;
         clearInterval(shapeInterval);
         shapeInterval = setInterval(createFallingShape, shapeDropRate);
     }

     if (timeLeft <= 0) {
         endGame();
     }
 }

 // Create a falling shape
 function createFallingShape() {
     if (!gameActive) return;

     const shape = document.createElement('div');
     shape.className = 'falling-shape';

     // Randomly decide if this will be the correct shape (30% chance)
     const isCorrect = Math.random() < 0.3;
     let shapeKey;

     if (typeof correctAnswer === 'number') {
         shapeKey = isCorrect ?
             (correctAnswer > 10 ? 10 : correctAnswer < 3 ? 3 : correctAnswer) :
             getRandomIncorrectShape();
     } else {
         // For non-number answers, use length of correct answer string
         const correctLength = correctAnswer.length;
         shapeKey = isCorrect ?
             (correctLength > 10 ? 10 : correctLength < 3 ? 3 : correctLength) :
             getRandomIncorrectShape();
     }

     shape.textContent = shapeImages[shapeKey];
     shape.style.fontSize = '50px';
     shape.style.textAlign = 'center';
     shape.style.lineHeight = '70px';
     shape.dataset.shapeValue = isCorrect ? 'correct' : 'wrong';

     // Random position at the top
     const leftPos = Math.random() * (window.innerWidth - 70);
     shape.style.left = `${leftPos}px`;
     shape.style.top = '-70px';

     gameArea.appendChild(shape);

     // Animation
     let currentTop = -70;
     const fallInterval = setInterval(() => {
         if (!gameActive) {
             clearInterval(fallInterval);
             return;
         }

         currentTop += shapeSpeed;
         shape.style.top = `${currentTop}px`;

         // Check if shape is caught
         const shapeRect = shape.getBoundingClientRect();
         const catcherRect = catcher.getBoundingClientRect();

         if (
             shapeRect.bottom >= catcherRect.top &&
             shapeRect.top <= catcherRect.bottom &&
             shapeRect.right >= catcherRect.left &&
             shapeRect.left <= catcherRect.right
         ) {
             clearInterval(fallInterval);
             shapeCaught(shape);
         }

         // Remove if out of screen
         if (currentTop > window.innerHeight) {
             clearInterval(fallInterval);
             shape.remove();
         }
     }, 16);
 }

 // Get a random incorrect shape
 function getRandomIncorrectShape() {
     let possibleShapes = Object.keys(shapeImages).map(Number);

     if (typeof correctAnswer === 'number') {
         possibleShapes = possibleShapes.filter(num => num !== correctAnswer);
     } else {
         // For non-number answers, filter by length
         const correctLength = correctAnswer.length;
         possibleShapes = possibleShapes.filter(num => num !== correctLength);
     }

     const randomIndex = Math.floor(Math.random() * possibleShapes.length);
     return possibleShapes[randomIndex];
 }

 // Handle shape caught
 function shapeCaught(shape) {
     shape.remove();

     if (shape.dataset.shapeValue === 'correct') {
         score += 10;
         playSound('catch-correct');
     } else {
         score -= 5;
         if (score < 0) score = 0;
         playSound('catch-wrong');
     }

     scoreDisplay.textContent = `Score: ${score}`;

     // Visual feedback
     const feedback = document.createElement('div');
     feedback.textContent = shape.dataset.shapeValue === 'correct' ? '+10' : '-5';
     feedback.style.position = 'absolute';
     feedback.style.left = `${parseInt(shape.style.left) + 35}px`;
     feedback.style.top = catcher.style.top;
     feedback.style.fontSize = '28px';
     feedback.style.fontWeight = 'bold';
     feedback.style.color = shape.dataset.shapeValue === 'correct' ? '#4CAF50' : '#d32f2f';
     feedback.style.zIndex = '4';
     gameArea.appendChild(feedback);

     // Animate feedback
     let opacity = 1;
     let currentTop = parseInt(catcher.style.top || '0');

     const feedbackInterval = setInterval(() => {
         opacity -= 0.05;
         currentTop -= 2;
         feedback.style.opacity = opacity;
         feedback.style.top = `${currentTop}px`;

         if (opacity <= 0) {
             clearInterval(feedbackInterval);
             feedback.remove();
         }
     }, 50);
 }

 // Move the catcher with mouse
 function moveCatcherMouse(e) {
     if (!gameActive) return;

     const catcherWidth = catcher.offsetWidth;
     let newLeft = e.clientX - catcherWidth / 2;

     // Keep within bounds
     newLeft = Math.max(0, Math.min(window.innerWidth - catcherWidth, newLeft));

     catcher.style.left = `${newLeft}px`;

     // Face direction of movement
     if (newLeft > parseInt(catcher.style.left || 0)) {
         catcher.style.transform = 'translateX(0) scaleX(1)';
     } else if (newLeft < parseInt(catcher.style.left || 0)) {
         catcher.style.transform = 'translateX(0) scaleX(-1)';
     }
 }

 // Move the catcher with touch
 function moveCatcherTouch(e) {
     if (!gameActive) return;
     e.preventDefault();

     const touch = e.touches[0];
     const catcherWidth = catcher.offsetWidth;
     let newLeft = touch.clientX - catcherWidth / 2;

     // Keep within bounds
     newLeft = Math.max(0, Math.min(window.innerWidth - catcherWidth, newLeft));

     catcher.style.left = `${newLeft}px`;

     // Face direction of movement
     if (newLeft > parseInt(catcher.style.left || 0)) {
         catcher.style.transform = 'translateX(0) scaleX(1)';
     } else if (newLeft < parseInt(catcher.style.left || 0)) {
         catcher.style.transform = 'translateX(0) scaleX(-1)';
     }
 }

 // End the game
 function endGame() {
     gameActive = false;
     clearInterval(gameInterval);
     clearInterval(shapeInterval);

     // Remove all falling shapes
     document.querySelectorAll('.falling-shape').forEach(shape => shape.remove());

     // Show game over screen
     gamePage.style.display = 'none';
     gameOverPage.style.display = 'flex';

     // Update game over display
     finalScoreDisplay.textContent = `Score: ${score}`;

     // Set target shape
     let shapeKey;
     if (typeof correctAnswer === 'number') {
         shapeKey = correctAnswer > 10 ? 10 : correctAnswer < 3 ? 3 : correctAnswer;
     } else {
         shapeKey = correctAnswer.length > 10 ? 10 : correctAnswer.length < 3 ? 3 : correctAnswer.length;
     }

     targetShapeResult.textContent = shapeImages[shapeKey];
     targetShapeResult.style.fontSize = '70px';
     shapeNameDisplay.textContent = shapeNames[shapeKey];

     // Calculate stars (1-3 based on score)
     const maxPossibleScore = 10 * (30 / (shapeDropRate / 1000)); // Approximate max score
     const starRatio = score / maxPossibleScore;

     starsDisplay.forEach((star, index) => {
         if (starRatio > (index + 1) / 3) {
             star.style.color = '#FFD700';
             star.style.transform = 'scale(1.2)';
             setTimeout(() => {
                 star.style.transform = 'scale(1)';
             }, 300);
         } else {
             star.style.color = '#ccc';
         }
     });

     // Update best scores display
     updateBestScoresDisplay();

     // Play sound based on performance
     if (starRatio > 0.66) {
         playSound('win');
     } else if (starRatio > 0.33) {
         playSound('medium');
     } else {
         playSound('lose');
     }
 }

 // Update the best scores display
 function updateBestScoresDisplay() {
     bestScoresList.innerHTML = '';

     // Sort questions by best score (highest first)
     const sortedQuestions = Object.entries(bestScores)
         .sort((a, b) => b[1] - a[1]);

     // Display top 5 or all if less than 5
     const displayCount = Math.min(5, sortedQuestions.length);

     for (let i = 0; i < displayCount; i++) {
         const [question, bestScore] = sortedQuestions[i];
         const scoreItem = document.createElement('div');
         scoreItem.className = 'best-score-item';
         scoreItem.innerHTML = `
                    <span>${question}...</span>
                    <span>${bestScore} points</span>
                `;
         bestScoresList.appendChild(scoreItem);
     }

     if (sortedQuestions.length === 0) {
         bestScoresList.innerHTML = '<p>No best scores yet. Keep playing!</p>';
     }
 }

 // Play again with same question
 function playAgain() {
     startGame();
 }

 // Go to next question
 function nextQuestion() {
     loadRandomQuestion();
     showMenuPage();
 }

 // Celebration effect for correct answer
 function celebrate() {
     const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6FF', '#DCEDC1'];

     for (let i = 0; i < 30; i++) {
         const confetti = document.createElement('div');
         confetti.style.position = 'absolute';
         confetti.style.width = '10px';
         confetti.style.height = '10px';
         confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
         confetti.style.borderRadius = '50%';
         confetti.style.left = `${Math.random() * 100}%`;
         confetti.style.top = '50%';
         confetti.style.zIndex = '100';
         confetti.style.transform = 'translate(-50%, -50%)';
         document.getElementById('question-box').appendChild(confetti);

         // Animate confetti
         const angle = Math.random() * Math.PI * 2;
         const velocity = 3 + Math.random() * 3;
         const xVel = Math.cos(angle) * velocity;
         const yVel = Math.sin(angle) * velocity;

         let xPos = 50;
         let yPos = 50;
         let opacity = 1;

         const animateConfetti = setInterval(() => {
             xPos += xVel;
             yPos += yVel;
             opacity -= 0.02;

             confetti.style.left = `${xPos}%`;
             confetti.style.top = `${yPos}%`;
             confetti.style.opacity = opacity;

             if (opacity <= 0) {
                 clearInterval(animateConfetti);
                 confetti.remove();
             }
         }, 50);
     }
 }

 // Play sound effects
 function playSound(type) {
     // In a real implementation, you would play actual sound files here
     console.log(`Playing sound: ${type}`);

     // For demonstration, we'll just log the sounds
     const sounds = {
         'correct': 'Yay!',
         'wrong': 'Oops!',
         'game-start': 'Boing!',
         'catch-correct': 'Ding!',
         'catch-wrong': 'Buzzer!',
         'win': 'Cheer!',
         'medium': 'Nice!',
         'lose': 'Aww...'
     };

     if (sounds[type]) {
         console.log(sounds[type]);
     }
 }

 // Initialize the game when the page loads
 window.addEventListener('load', () => {
     homeScreen.style.display = 'flex';
     initGame();
 });