document.addEventListener('DOMContentLoaded', () => {
    const questions = [
        {
            question: "Match the Surface Area Formulas",
            items: [
                { id: "q1-item1", text: "Surface area of a cube" },
                { id: "q1-item2", text: "Surface area of a rectangular prism" },
                { id: "q1-item3", text: "Surface area of a sphere" },
                { id: "q1-item4", text: "Surface area of a cylinder" }
            ],
            answers: [
                { id: "q1-answer1", text: "6a^2" },
                { id: "q1-answer2", text: "2lw + 2lh + 2wh" },
                { id: "q1-answer3", text: "4πr^2" },
                { id: "q1-answer4", text: "2πr(h + r)" }
            ]
        },
        {
            question: "Match the Volume Formulas",
            items: [
                { id: "q2-item1", text: "Volume of a cube" },
                { id: "q2-item2", text: "Volume of a rectangular prism" },
                { id: "q2-item3", text: "Volume of a sphere" },
                { id: "q2-item4", text: "Volume of a cylinder" }
            ],
            answers: [
                { id: "q2-answer1", text: "a^3" },
                { id: "q2-answer2", text: "lwh" },
                { id: "q2-answer3", text: "(4/3)πr^3" },
                { id: "q2-answer4", text: "πr^2h" }
            ]
        },
        {
            question: "Match the Surface Area Formulas",
            items: [
                { id: "q3-item1", text: "Surface area of a cone" },
                { id: "q3-item2", text: "Surface area of a pyramid" },
                { id: "q3-item3", text: "Surface area of a triangular prism" },
                { id: "q3-item4", text: "Surface area of a hemisphere" }
            ],
            answers: [
                { id: "q3-answer1", text: "πr(r + l)" },
                { id: "q3-answer2", text: "Base area + 1/2 * Perimeter * Slant height" },
                { id: "q3-answer3", text: "Base area + Lateral area" },
                { id: "q3-answer4", text: "3πr^2" }
            ]
        },
        {
            question: "Match the Volume Formulas",
            items: [
                { id: "q4-item1", text: "Volume of a cone" },
                { id: "q4-item2", text: "Volume of a pyramid" },
                { id: "q4-item3", text: "Volume of a triangular prism" },
                { id: "q4-item4", text: "Volume of a hemisphere" }
            ],
            answers: [
                { id: "q4-answer1", text: "(1/3)πr^2h" },
                { id: "q4-answer2", text: "(1/3)Base area * Height" },
                { id: "q4-answer3", text: "Base area * Height" },
                { id: "q4-answer4", text: "(2/3)πr^3" }
            ]
        },
        {
            question: "Match the Perimeter Formulas",
            items: [
                { id: "q5-item1", text: "Perimeter of a square" },
                { id: "q5-item2", text: "Perimeter of a rectangle" },
                { id: "q5-item3", text: "Perimeter of a triangle" },
                { id: "q5-item4", text: "Perimeter of a circle" }
            ],
            answers: [
                { id: "q5-answer1", text: "4a" },
                { id: "q5-answer2", text: "2(l + w)" },
                { id: "q5-answer3", text: "a + b + c" },
                { id: "q5-answer4", text: "2πr" }
            ]
        },
        {
            question: "Match the Perimeter Formulas",
            items: [
                { id: "q6-item1", text: "Perimeter of a parallelogram" },
                { id: "q6-item2", text: "Perimeter of a trapezoid" },
                { id: "q6-item3", text: "Perimeter of an equilateral triangle" },
                { id: "q6-item4", text: "Perimeter of a regular hexagon" }
            ],
            answers: [
                { id: "q6-answer1", text: "2(a + b)" },
                { id: "q6-answer2", text: "a + b + c + d" },
                { id: "q6-answer3", text: "3a" },
                { id: "q6-answer4", text: "6a" }
            ]
        },
        {
            question: "Match the Surface Area Formulas",
            items: [
                { id: "q7-item1", text: "Surface area of a rectangular prism" },
                { id: "q7-item2", text: "Surface area of a triangular prism" },
                { id: "q7-item3", text: "Surface area of a pentagonal prism" },
                { id: "q7-item4", text: "Surface area of a hexagonal prism" }
            ],
            answers: [
                { id: "q7-answer1", text: "2lw + 2lh + 2wh" },
                { id: "q7-answer2", text: "Base area + Lateral area" },
                { id: "q7-answer3", text: "5a^2" },
                { id: "q7-answer4", text: "6a^2" }
            ]
        },
        {
            question: "Match the Volume Formulas",
            items: [
                { id: "q8-item1", text: "Volume of a cube" },
                { id: "q8-item2", text: "Volume of a sphere" },
                { id: "q8-item3", text: "Volume of a cone" },
                { id: "q8-item4", text: "Volume of a cylinder" }
            ],
            answers: [
                { id: "q8-answer1", text: "a^3" },
                { id: "q8-answer2", text: "(4/3)πr^3" },
                { id: "q8-answer3", text: "(1/3)πr^2h" },
                { id: "q8-answer4", text: "πr^2h" }
            ]
        },
        {
            question: "Match the Perimeter Formulas",
            items: [
                { id: "q9-item1", text: "Perimeter of a rhombus" },
                { id: "q9-item2", text: "Perimeter of a kite" },
                { id: "q9-item3", text: "Perimeter of a regular octagon" },
                { id: "q9-item4", text: "Perimeter of a regular decagon" }
            ],
            answers: [
                { id: "q9-answer1", text: "4a" },
                { id: "q9-answer2", text: "2(a + b)" },
                { id: "q9-answer3", text: "8a" },
                { id: "q9-answer4", text: "10a" }
            ]
        },
        {
            question: "Match the Surface Area Formulas",
            items: [
                { id: "q10-item1", text: "Surface area of a rhombus" },
                { id: "q10-item2", text: "Surface area of a kite" },
                { id: "q10-item3", text: "Surface area of a regular octagon" },
                { id: "q10-item4", text: "Surface area of a regular decagon" }
            ],
            answers: [
                { id: "q10-answer1", text: "4a^2" },
                { id: "q10-answer2", text: "1/2 * d1 * d2" },
                { id: "q10-answer3", text: "2a^2(1 + √2)" },
                { id: "q10-answer4", text: "5a^2(1 + 2√5)" }
            ]
        }
    ];

    const selectedQuestions = selectRandomQuestions(questions, 4);
    initializeGame(selectedQuestions);

    function selectRandomQuestions(data, numQuestions) {
        const shuffled = data.sort(() => 0.5 - Math.random());
        return shuffled.slice(0, numQuestions);
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    function initializeGame(data) {
        const gameContainer = document.getElementById('game-container');
        
        data.forEach((questionData, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.classList.add('question');
            if (index === 0) questionDiv.classList.add('active');
            questionDiv.id = `question${index + 1}`;

            const questionTitle = document.createElement('h2');
            questionTitle.textContent = questionData.question;
            questionDiv.appendChild(questionTitle);

            const questionsColumn = document.createElement('div');
            questionsColumn.classList.add('column');
            questionsColumn.id = `q${index + 1}-questions`;

            // Shuffle items
            const shuffledItems = shuffleArray([...questionData.items]);
            shuffledItems.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.classList.add('item');
                itemDiv.draggable = true;
                itemDiv.id = item.id;
                itemDiv.textContent = item.text;
                questionsColumn.appendChild(itemDiv);
            });

            const answersColumn = document.createElement('div');
            answersColumn.classList.add('column');
            answersColumn.id = `q${index + 1}-answers`;

            // Shuffle answers
            const shuffledAnswers = shuffleArray([...questionData.answers]);
            shuffledAnswers.forEach(answer => {
                const answerDiv = document.createElement('div');
                answerDiv.classList.add('dropzone');
                answerDiv.id = answer.id;
                answerDiv.textContent = answer.text;
                answersColumn.appendChild(answerDiv);
            });

            questionDiv.appendChild(questionsColumn);
            questionDiv.appendChild(answersColumn);

            if (index < data.length - 1) {
                const nextButton = document.createElement('button');
                nextButton.classList.add('next');
                nextButton.id = `next${index + 1}`;
                nextButton.textContent = 'Next';
                nextButton.addEventListener('click', () => showQuestion(index + 1));
                questionDiv.appendChild(nextButton);
            } else {
                const submitButton = document.createElement('button');
                submitButton.id = 'submit';
                submitButton.textContent = 'Submit';
                submitButton.addEventListener('click', () => calculateScore(data));
                questionDiv.appendChild(submitButton);
            }

            const resetButton = document.createElement('button');
            resetButton.classList.add('reset');
            resetButton.id = `reset${index + 1}`;
            resetButton.textContent = 'Reset';
            resetButton.addEventListener('click', () => resetCurrentQuestion(index + 1));
            questionDiv.appendChild(resetButton);

            gameContainer.appendChild(questionDiv);
        });

        // Initialize drag and drop functionality
        initializeDragAndDrop();
    }

    function initializeDragAndDrop() {
        const items = document.querySelectorAll('.item[draggable="true"]');
        const dropzones = document.querySelectorAll('.dropzone');

        items.forEach(item => {
            item.addEventListener('dragstart', dragStart);
        });

        dropzones.forEach(dropzone => {
            dropzone.addEventListener('dragover', dragOver);
            dropzone.addEventListener('drop', drop);
        });
    }

    function dragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.id);
        e.target.classList.add('dragging');
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function drop(e) {
        e.preventDefault();
        const itemId = e.dataTransfer.getData('text/plain');
        const draggedElement = document.getElementById(itemId);
        const targetElement = e.target;

        if (targetElement.classList.contains('dropzone')) {
            targetElement.appendChild(draggedElement);
        }

        draggedElement.classList.remove('dragging');
    }

    function calculateScore(data) {
        console.log("Submit button clicked");
        let score = 0;

        data.forEach((questionData, index) => {
            questionData.items.forEach(item => {
                const itemElement = document.getElementById(item.id);
                const correctAnswer = questionData.answers.find(answer => answer.id === item.id.replace('item', 'answer'));
                const answerElement = document.getElementById(correctAnswer.id);

                console.log(`Checking item ${item.id} in answer ${correctAnswer.id}`);
                if (answerElement && answerElement.contains(itemElement)) {
                    console.log(`Item ${item.id} is correctly placed in ${correctAnswer.id}`);
                    score++;
                } else {
                    console.log(`Item ${item.id} is NOT correctly placed in ${correctAnswer.id}`);
                }
            });
        });

        console.log(`Score calculated: ${score}`);
        const total = data.reduce((acc, question) => acc + question.items.length, 0);
        window.location.href = `result.html?score=${score}&total=${total}`;
    }

    function resetCurrentQuestion(questionIndex) {
        const questionItems = document.querySelectorAll(`#question${questionIndex} .item`);
        const questionsColumn = document.getElementById(`q${questionIndex}-questions`);
        questionItems.forEach(item => {
            questionsColumn.appendChild(item);
        });
    }

    function showQuestion(index) {
        const questions = document.querySelectorAll('.question');
        questions.forEach((question, i) => {
            question.classList.toggle('active', i === index);
        });
    }
});