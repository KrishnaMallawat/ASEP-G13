let score = 0;
let ordersCompleted = 0;
let correctAnswers = 0;
let currentQuestion = {};
let timeLeft = 60;
let timer;
let gameActive = false;
let starsEarned = 0;
let selectedWeight = 0;
let weightBlocksVisible = false;
let selectedLength = 0;
let lengthBlocksVisible = false;

// DOM elements
const speechBubble = document.querySelector('.speech-bubble');
const customer = document.querySelector('.customer');
const answerOptions = document.querySelector('.answer-options');
const feedback = document.querySelector('.feedback');
const scoreDisplay = document.querySelector('.score');
const ordersDisplay = document.querySelector('.orders-completed');
const timeDisplay = document.querySelector('.time');
const startScreen = document.querySelector('.start-screen');
const levelCompleteScreen = document.querySelector('.level-complete');
const completedOrdersDisplay = document.querySelector('.completed-orders');
const accuracyDisplay = document.querySelector('.accuracy');
const starsEarnedDisplay = document.querySelector('.stars-earned');
const confettiCanvas = document.querySelector('.confetti');
const successSound = document.getElementById('success-sound');
const failSound = document.getElementById('fail-sound');
const weightBlocksContainer = document.querySelector('.weight-blocks');
const weightBlockButtons = document.querySelectorAll('.weight-block');

const selectedWeightDisplay = document.querySelector('.selected-weight');
const submitWeightButton = document.querySelector('.submit-weight');
const resetWeightButton = document.querySelector('.reset-weight');
// Fix: Use correct selectors for length blocks
const lengthBlocksContainer = document.querySelector('.length-blocks');
const lengthBlockButtons = document.querySelectorAll('.length-block');
const selectedLengthDisplay = document.querySelector('.selected-length');
const submitLengthButton = document.querySelector('.submit-length');
const resetLengthButton = document.querySelector('.reset-length');

// Cartoon customer images
const customerImages = [
    'https://img.freepik.com/free-vector/cute-cat-chef-cartoon-vector-icon-illustration_138676-6181.jpg',
    'https://img.freepik.com/free-vector/cute-rabbit-cartoon-vector-icon-illustration_138676-5723.jpg',
    'https://img.freepik.com/free-vector/cute-fox-cartoon-vector-icon-illustration_138676-5558.jpg',
    'https://img.freepik.com/free-vector/cute-owl-cartoon-vector-icon-illustration_138676-5640.jpg'
];

// Cartoon food images for options
const foodImages = [
    'https://img.icons8.com/color/96/000000/cupcake.png',
    'https://img.icons8.com/color/96/000000/pizza.png',
    'https://img.icons8.com/color/96/000000/doughnut.png',
    'https://img.icons8.com/color/96/000000/apple.png',
    'https://img.icons8.com/color/96/000000/banana.png',
    'https://img.icons8.com/color/96/000000/cheese.png',
    'https://img.icons8.com/color/96/000000/broccoli.png',
    'https://img.icons8.com/color/96/000000/carrot.png'
];

// Questions for 5th grade level
const questions = [{
    question: "Can I have 2 kilograms of flour in grams?",
    fromUnit: "kg",
    toUnit: "g",
    value: 2,
    answer: 2000
}, {
    question: "I need 3 kilograms of sugar in grams.",
    fromUnit: "kg",
    toUnit: "g",
    value: 3,
    answer: 3000
}, {
    question: "Please give me 1.5 kilograms of rice in grams.",
    fromUnit: "kg",
    toUnit: "g",
    value: 1.5,
    answer: 1500
}, {
    question: "I'd like 0.75 kilograms of butter in grams.",
    fromUnit: "kg",
    toUnit: "g",
    value: 0.75,
    answer: 750
}, {
    question: "Can you prepare 0.5 kilograms of tea in grams?",
    fromUnit: "kg",
    toUnit: "g",
    value: 0.5,
    answer: 500
}, {
    question: "How many centimeters are in 2 kilometers?",
    fromUnit: "km",
    toUnit: "cm",
    value: 2,
    answer: 200000
}, {
    question: "Convert 3 kilometers to centimeters.",
    fromUnit: "km",
    toUnit: "cm",
    value: 3,
    answer: 300000
}, {
    question: "How many centimeters are in 0.8 kilometers?",
    fromUnit: "km",
    toUnit: "cm",
    value: 0.8,
    answer: 80000
}, {
    question: "I'd like 1.25 kilometers in centimeters.",
    fromUnit: "km",
    toUnit: "cm",
    value: 1.25,
    answer: 125000
}, {
    question: "Can you prepare 0.5 kilometers in centimeters?",
    fromUnit: "km",
    toUnit: "cm",
    value: 0.5,
    answer: 50000
}, {
    question: "How many centimeters are in 2 meters?",
    fromUnit: "m",
    toUnit: "cm",
    value: 2,
    answer: 200
}, {
    question: "Convert 3.5 meters to centimeters.",
    fromUnit: "m",
    toUnit: "cm",
    value: 3.5,
    answer: 350
}, {
    question: "How many centimeters are in 0.75 meters?",
    fromUnit: "m",
    toUnit: "cm",
    value: 0.75,
    answer: 75
}, {
    question: "I'd like 1.2 meters in centimeters.",
    fromUnit: "m",
    toUnit: "cm",
    value: 1.2,
    answer: 120
}, {
    question: "Can you prepare 0.6 meters in centimeters?",
    fromUnit: "m",
    toUnit: "cm",
    value: 0.6,
    answer: 60
}];

// --- Quit Button Logic ---
function openQuitConfirm() {
    document.getElementById('quit-confirm-overlay').style.display = 'flex';
}

function closeQuitConfirm() {
    document.getElementById('quit-confirm-overlay').style.display = 'none';
}

function quitGame() {
    document.getElementById('game-container').style.display = 'none';
    document.getElementById('quit-confirm-overlay').style.display = 'none';
    let bye = document.createElement('div');
    bye.style.position = 'fixed';
    bye.style.top = '0';
    bye.style.left = '0';
    bye.style.width = '100vw';
    bye.style.height = '100vh';
    bye.style.background = 'linear-gradient(120deg,#FFD700,#FFB347,#fffbe6)';
    bye.style.display = 'flex';
    bye.style.flexDirection = 'column';
    bye.style.alignItems = 'center';
    bye.style.justifyContent = 'center';
    bye.style.zIndex = '9999';
    bye.innerHTML = `<h1 style="color:#FF6347;font-size:3vw;font-family:'Fredoka One',cursive;text-shadow:2px 2px #FFD700;">Thanks for playing!</h1>
            <p style="color:#FF6347;font-size:2vw;font-family:'Fredoka One',cursive;">You have quit the Unit Converter Cartoon Café.</p>`;
    document.body.appendChild(bye);
}

// --- Weight Block Logic ---
function handleWeightBlockClick(weight) {
    selectedWeight += parseInt(weight);
    updateSelectedWeightDisplay();
}

function updateSelectedWeightDisplay() {
    selectedWeightDisplay.textContent = selectedWeight;
}

function resetWeightSelection() {
    selectedWeight = 0;
    updateSelectedWeightDisplay();
}

function submitWeightAnswer() {
    if (!gameActive) return;
    checkAnswer(selectedWeight, false);
    hideWeightBlocks();
}

function showWeightBlocks() {
    weightBlocksContainer.style.display = 'flex';
    weightBlocksVisible = true;
    resetWeightSelection();
}

function hideWeightBlocks() {
    weightBlocksContainer.style.display = 'none';
    weightBlocksVisible = false;
}

// Add event listeners for weight blocks
weightBlockButtons.forEach(button => {
    button.addEventListener('click', () => handleWeightBlockClick(button.dataset.weight));
});

submitWeightButton.addEventListener('click', submitWeightAnswer);
resetWeightButton.addEventListener('click', resetWeightSelection);
// Fix: Use correct data attribute for length blocks
lengthBlockButtons.forEach(button => {
    button.addEventListener('click', () => handleLengthBlockClick(button.dataset.length));
});
submitLengthButton.addEventListener('click', submitLengthAnswer);
resetLengthButton.addEventListener('click', resetLengthSelection);


// Utility: shuffle array
function shuffle(array) {
    let currentIndex = array.length,
        randomIndex;
    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
}

function handleLengthBlockClick(length) {
    selectedLength += parseInt(length);
    updateSelectedLengthDisplay();
}

function updateSelectedLengthDisplay() {
    selectedLengthDisplay.textContent = selectedLength;
}

function resetLengthSelection() {
    selectedLength = 0;
    updateSelectedLengthDisplay();
}

function submitLengthAnswer() {
    if (!gameActive) return;
    checkAnswer(selectedLength, false);
    hideLengthBlocks();
}

function showLengthBlocks() {
    lengthBlocksContainer.style.display = 'flex';
    lengthBlocksVisible = true;
    resetLengthSelection();
}

function hideLengthBlocks() {
    lengthBlocksContainer.style.display = 'none';
    lengthBlocksVisible = false;
}

// Start game
document.querySelector('.start-btn').addEventListener('click', startGame);
document.querySelector('.next-level-btn').addEventListener('click', startGame);

function startGame() {
    score = 0;
    ordersCompleted = 0;
    correctAnswers = 0;
    timeLeft = 60; // <-- Corrected from 10 to 60
    starsEarned = 0;
    scoreDisplay.textContent = score;
    ordersDisplay.textContent = `${ordersCompleted}/10`;
    timeDisplay.textContent = timeLeft;
    startScreen.style.display = 'none';
    levelCompleteScreen.style.display = 'none';
    gameActive = true;
    clearInterval(timer);
    timer = setInterval(updateTimer, 1000);
    showNextCustomer();
}

function updateTimer() {
    timeLeft--;

    timeDisplay.textContent = timeLeft;
    if (timeLeft <= 0) {
        clearInterval(timer);
        endGame();
    }
}

function showNextCustomer() {
    hideWeightBlocks();
    const randomCustomer = customerImages[Math.floor(Math.random() * customerImages.length)];
    customer.querySelector('img').src = randomCustomer;
    customer.classList.add('customer-enter');
    const randomIndex = Math.floor(Math.random() * questions.length);
    currentQuestion = questions[randomIndex];
    speechBubble.textContent = currentQuestion.question;
    generateOptions();
    setTimeout(() => {
        speechBubble.style.opacity = '1';
        customer.classList.remove('customer-enter');
    }, 500);
}

function isLengthQuestion(q) {
    return ['km', 'm', 'cm', 'mm'].includes(q.fromUnit) || ['km', 'm', 'cm', 'mm'].includes(q.toUnit);
}

function generateOptions() {
    answerOptions.innerHTML = '';
    const isMass = ['kg', 'g'].includes(currentQuestion.fromUnit) || ['kg', 'g'].includes(currentQuestion.toUnit);
    const isLength = isLengthQuestion(currentQuestion);

    if (isMass) {
        showWeightBlocks();
        hideLengthBlocks();
    } else if (isLength) {
        hideWeightBlocks();
        showLengthBlocks();
    } else {
        hideWeightBlocks();
        hideLengthBlocks();
        // ... (existing option generation logic for other unit types)
    }
}

function pickOption(opt, div) {
    if (!gameActive) return;
    if (answerOptions.classList.contains('locked')) return; // Prevent double click
    answerOptions.classList.add('locked');
    document.querySelectorAll('.food-option').forEach(el => {
        el.classList.remove('selected', 'incorrect', 'disabled');
    });
    let correct = Math.abs(opt - currentQuestion.answer) < 0.01;
    if (correct) {
        div.classList.add('selected');
        playConfetti();
        successSound.currentTime = 0;
        successSound.play();
    } else {
        div.classList.add('incorrect');
        failSound.currentTime = 0;
        failSound.play();
        setTimeout(() => {
            document.querySelectorAll('.food-option').forEach(el => {
                if (Math.abs(parseFloat(el.innerText) - currentQuestion.answer) < 0.01) {
                    el.classList.add('selected');
                }
            });
        }, 350);
    }
    document.querySelectorAll('.food-option').forEach(el => el.classList.add('disabled'));
    setTimeout(() => {
        answerOptions.classList.remove('locked');
        checkAnswer(opt, true);
    }, 900);
}

function checkAnswer(userAnswer, isOption) {
    if (!gameActive) return;
    let correct = Math.abs(userAnswer - currentQuestion.answer) < 0.01;
    if (correct) {
        feedback.textContent = "🎉 Perfect! Thank you! 🎉";
        feedback.className = "feedback positive-feedback";
        score += 10;
        correctAnswers++;
        timeDisplay.textContent = timeLeft;
        scoreDisplay.textContent = score;
    } else {
        feedback.textContent = `😅 Oops! It's ${currentQuestion.answer} ${currentQuestion.toUnit}.`;
        feedback.className = "feedback negative-feedback";
        score = Math.max(0, score - 5);
        timeDisplay.textContent = timeLeft;
        scoreDisplay.textContent = score;
    }
    ordersCompleted++;
    ordersDisplay.textContent = `${ordersCompleted}/10`;
    feedback.style.opacity = '1';
    setTimeout(() => {
        feedback.style.opacity = '0';
        if (ordersCompleted >= 10) {
            endGame();
        } else {
            customer.classList.add('customer-exit');
            speechBubble.style.opacity = '0';
            setTimeout(() => {
                customer.classList.remove('customer-exit');
                showNextCustomer();
            }, 1000);
        }
    }, 1700);
}

function endGame() {
    gameActive = false;
    clearInterval(timer);
    starsEarned = Math.min(5, Math.floor(correctAnswers / 2));
    completedOrdersDisplay.textContent = ordersCompleted;
    accuracyDisplay.textContent = ordersCompleted > 0 ? Math.round((correctAnswers / ordersCompleted) * 100) : 0;
    starsEarnedDisplay.textContent = starsEarned;
    levelCompleteScreen.style.display = 'flex';
    showStars();
}

function showStars() {
    let starsContainer = document.querySelector('.level-complete .instructions');
    let existing = starsContainer.querySelector('.progress-bar');
    if (existing) existing.remove();
    let starsDiv = document.createElement('div');
    starsDiv.className = 'progress-bar';
    for (let i = 0; i < 5; i++) {
        let star = document.createElement('span');
        star.className = 'star';
        star.textContent = i < starsEarned ? '★' : '☆';
        if (i < starsEarned) star.classList.add('filled');
        starsDiv.appendChild(star);
    }
    starsContainer.appendChild(starsDiv);
}

function playConfetti() {
    let canvas = confettiCanvas;
    let W = window.innerWidth,
        H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;
    canvas.style.display = 'block';
    let ctx = canvas.getContext('2d');
    let pieces = [];
    for (let i = 0; i < 120; i++) {
        pieces.push({
            x: Math.random() * W,
            y: Math.random() * -H,
            r: 6 + Math.random() * 10,
            d: Math.random() * 100,
            color: `hsl(${Math.random()*360},90%,60%)`,
            tilt: Math.random() * 20 - 10,
            tiltAngle: 0,
            tiltAngleIncremental: (Math.random() * 0.07) + .05
        });
    }
    let angle = 0;

    function draw() {
        ctx.clearRect(0, 0, W, H);
        for (let i = 0; i < pieces.length; i++) {
            let p = pieces[i];
            ctx.beginPath();
            ctx.lineWidth = p.r;
            ctx.strokeStyle = p.color;
            ctx.moveTo(p.x + p.tilt + (p.r / 3), p.y);
            ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r);
            ctx.stroke();
        }
        update();
    }

    function update() {
        angle += 0.01;
        for (let i = 0; i < pieces.length; i++) {
            let p = pieces[i];
            p.y += (Math.cos(angle + p.d) + 3 + p.r / 2) / 2;
            p.x += Math.sin(angle);
            p.tiltAngle += p.tiltAngleIncremental;
            p.tilt = Math.sin(p.tiltAngle) * 15;
            if (p.y > H) {
                p.x = Math.random() * W;
                p.y = -10;
            }
        }
    }
    let count = 0;

    function animate() {
        draw();
        count++;
        if (count < 60) requestAnimationFrame(animate);
        else canvas.style.display = 'none';
    }
    animate();
}
showStars();