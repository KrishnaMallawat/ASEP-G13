let hour = 12;
let minute = 0;
let targetHour, targetMinute;
let questionCount = 0;
const totalQuestions = 5;
let results = [];

// List of tricky time expressions with placeholders for random hours
const trickyTimePatterns = [
    { 
        text: "Quarter to X", 
        minute: 45, 
        hourOffset: -1, 
        fact: "At 8:45 AM on August 15, 1947, India celebrated its first day of independence from British rule." 
    },
    { 
        text: "Quarter past X", 
        minute: 15, 
        hourOffset: 0, 
        fact: "At 10:15 AM on July 21, 1969, Rakesh Sharma was selected to become the first Indian to go to space." 
    },
    { 
        text: "Half past X", 
        minute: 30, 
        hourOffset: 0, 
        fact: "At 12:30 PM on January 26, 1950, Dr. Rajendra Prasad was sworn in as the first President of India, marking the birth of the Indian Republic." 
    },
    { 
        text: "Ten minutes to X", 
        minute: 50, 
        hourOffset: -1, 
        fact: "At 4:50 PM on October 20, 1988, India launched its first indigenous satellite, INSAT-1C, marking a milestone in its space program." 
    },
    { 
        text: "Twenty minutes past X", 
        minute: 20, 
        hourOffset: 0, 
        fact: "At 7:20 AM on May 18, 1974, India conducted its first peaceful nuclear test under the Smiling Buddha program." 
    },
    { 
        text: "Five minutes past X", 
        minute: 5, 
        hourOffset: 0, 
        fact: "At 6:05 PM on June 25, 1983, India won its first Cricket World Cup, defeating the West Indies." 
    },
    { 
        text: "Twenty-five minutes to X", 
        minute: 35, 
        hourOffset: -1, 
        fact: "At 2:35 PM on November 14, 1889, Jawaharlal Nehru was born, who later became India's first Prime Minister and a symbol of progress and education." 
    },
    { 
        text: "Ten minutes past X", 
        minute: 10, 
        hourOffset: 0, 
        fact: "At 10:10 AM on February 24, 2019, ISRO launched its PSLV-C45 satellite mission, showcasing India's advancement in space technology." 
    }
];

function generateRandomTrickyTime() {
    // Clear previous result message before showing a new question
    document.getElementById("result-message").innerText = "";  

    // Pick a random tricky time pattern
    let randomIndex = Math.floor(Math.random() * trickyTimePatterns.length);
    let selectedPattern = trickyTimePatterns[randomIndex];

    // Randomize the base hour (1-12)
    let baseHour = Math.floor(Math.random() * 12) + 1;

    // Calculate the target hour and minute
    targetMinute = selectedPattern.minute;

    // Adjust hour for "to" expressions
    targetHour = (baseHour + selectedPattern.hourOffset + 12) % 12 || 12;

    // Replace "X" in the text with the base hour
    let questionText = selectedPattern.text.replace("X", baseHour);
    document.getElementById("question-time").innerText = questionText;
}

function changeTime(type, value) {
    if (type === 'hour') {
        hour = (hour + value + 12) % 12 || 12;
    } else if (type === 'minute') {
        minute = (minute + value + 60) % 60;
    }
    updateClock();
}

function updateClock() {
    const hourDegree = (hour % 12) * 30 + (minute / 60) * 30;
    const minuteDegree = minute * 6;

    document.getElementById("hour-hand").style.transform = 
        `translateX(-50%) rotate(${hourDegree}deg)`;
    document.getElementById("minute-hand").style.transform = 
        `translateX(-50%) rotate(${minuteDegree}deg)`;
}

function checkTime() {
    let correct = (hour === targetHour && minute === targetMinute);

    if (correct) {
        // Find the matching pattern to get the historical fact
        let fact = trickyTimePatterns.find(pattern => 
            pattern.minute === targetMinute && 
            pattern.hourOffset === (hour === targetHour ? 0 : -1)
        )?.fact;

        if (fact) {
            alert(`✅ Correct! Here's a fact: \n${fact}`);
        } else {
            alert("✅ Correct!");
        }
    } else {
        alert("❌ Wrong!");
    }

    results.push({
        targetHour,
        targetMinute,
        userHour: hour,
        userMinute: minute,
        correct
    });

    document.getElementById("result-message").innerText = correct ? "✅ Correct!" : "❌ Wrong!";

    questionCount++;
    if (questionCount >= totalQuestions) {
        localStorage.setItem("quizResults", JSON.stringify(results));
        window.location.href = "Results.html";
    } else {
        setTimeout(generateRandomTrickyTime, 1000);
    }
}

generateRandomTrickyTime();
updateClock();
