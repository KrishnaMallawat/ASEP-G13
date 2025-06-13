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

    // Function to select random questions
    function selectRandomQuestions(data, numQuestions) {
        return data.sort(() => 0.5 - Math.random()).slice(0, numQuestions);
    }

    // Function to shuffle an array
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    // Function to initialize the game
    function initializeGame(data) {
        const gameContainer = document.getElementById('game-container');
        const buttonContainer = document.getElementById('button-container');
        const questionTitle = document.getElementById('question-title');
        
        data.forEach((questionData, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.classList.add('question');
            if (index === 0) {
                questionDiv.classList.add('active');
                questionTitle.textContent = questionData.question;
            }
            questionDiv.id = `question${index + 1}`;

            const questionsColumn = document.createElement('div');
            questionsColumn.classList.add('column');
            questionsColumn.id = `q${index + 1}-questions`;

            shuffleArray([...questionData.items]).forEach(item => {
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

            shuffleArray([...questionData.answers]).forEach(answer => {
                const answerDiv = document.createElement('div');
                answerDiv.classList.add('dropzone');
                answerDiv.id = answer.id;
                answerDiv.textContent = answer.text;
                answersColumn.appendChild(answerDiv);
            });

            questionDiv.appendChild(questionsColumn);
            questionDiv.appendChild(answersColumn);
            gameContainer.appendChild(questionDiv);
        });

        // Create and initialize the Next button
        const nextButton = document.createElement('button');
        nextButton.classList.add('button', 'next');
        nextButton.id = 'next-button';
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', () => showNextQuestion(data));
        buttonContainer.appendChild(nextButton);

        // Create and initialize the Submit button
        const submitButton = document.createElement('button');
        submitButton.classList.add('button');
        submitButton.id = 'submit-button';
        submitButton.textContent = 'Submit';
        submitButton.addEventListener('click', () => calculateScore(data));
        submitButton.style.display = 'none';
        buttonContainer.appendChild(submitButton);

        // Create and initialize the Reset button
        const resetButton = document.createElement('button');
        resetButton.classList.add('button', 'reset');
        resetButton.id = 'reset-button';
        resetButton.textContent = 'Reset';
        resetButton.addEventListener('click', resetCurrentQuestion);
        buttonContainer.appendChild(resetButton);

        // Initialize drag and drop functionality
        initializeDragAndDrop();
    }

    // Function to initialize drag and drop functionality
    function initializeDragAndDrop() {
        document.querySelectorAll('.item[draggable="true"]').forEach(item => {
            item.addEventListener('dragstart', dragStart);
        });

        document.querySelectorAll('.dropzone').forEach(dropzone => {
            dropzone.addEventListener('dragover', dragOver);
            dropzone.addEventListener('drop', drop);
        });
    }

    // Function to handle drag start event
    function dragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.id);
        e.target.classList.add('dragging');
    }

    // Function to handle drag over event
    function dragOver(e) {
        e.preventDefault();
    }

    // Function to handle drop event
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

    // Function to calculate the score
    function calculateScore(data) {
        let score = 0;

        data.forEach((questionData) => {
            questionData.items.forEach(item => {
                const itemElement = document.getElementById(item.id);
                const correctAnswer = questionData.answers.find(answer => answer.id === item.id.replace('item', 'answer'));
                const answerElement = document.getElementById(correctAnswer.id);

                if (answerElement && answerElement.contains(itemElement)) {
                    score++;
                }
            });
        });

        const total = data.reduce((acc, question) => acc + question.items.length, 0);
        // Use Flask route for results page
        window.location.href = '/results';
    }

    // Function to reset the current question
    function resetCurrentQuestion() {
        const activeQuestion = document.querySelector('.question.active');
        const questionIndex = Array.from(activeQuestion.parentNode.children).indexOf(activeQuestion) + 1;
        const questionItems = document.querySelectorAll(`#question${questionIndex} .item`);
        const questionsColumn = document.getElementById(`q${questionIndex}-questions`);
        questionItems.forEach(item => {
            questionsColumn.appendChild(item);
        });
    }

    // Function to show the next question
    function showNextQuestion(data) {
        const activeQuestion = document.querySelector('.question.active');
        const questionIndex = Array.from(activeQuestion.parentNode.children).indexOf(activeQuestion);
        const questionTitle = document.getElementById('question-title');
        if (questionIndex < data.length - 1) {
            activeQuestion.classList.remove('active');
            activeQuestion.nextElementSibling.classList.add('active');
            questionTitle.textContent = data[questionIndex + 1].question;
            if (questionIndex === data.length - 2) {
                document.getElementById('next-button').style.display = 'none';
                document.getElementById('submit-button').style.display = 'inline-block';
            }
        }
    }
});