setInterval(() => {
    console.log("Generating new elements...");

    let cloneCount = 10; 
    let minDistance = 50; 
    let existingPositions = []; 
    for (let i = 0; i < cloneCount; i++) {
        let span = document.createElement("span");
        span.classList.add("animated-background");
        let images = ["pi.png", "pi2.png", "pi3.png"];
        let randomImage = images[Math.floor(Math.random() * images.length)];
        span.style.backgroundImage = `url('static/${randomImage}')`;

        let uniqueID = "falling-" + Date.now() + "-" + i;
        span.id = uniqueID;

        let randomLeft;
        let maxAttempts = 5;
        let attempts = 0;
        let tooClose;

        do {
            tooClose = false;
            randomLeft = Math.floor(Math.random() * (window.innerWidth - 50)) + "px"; // Adjust based on screen width
            let randomLeftValue = parseInt(randomLeft);

            for (let pos of existingPositions) {
                if (Math.abs(pos - randomLeftValue) < minDistance) {
                    tooClose = true;
                    break;
                }
            }
            attempts++;
        } while (tooClose && attempts < maxAttempts);

        existingPositions.push(parseInt(randomLeft)); 
        span.style.left = randomLeft;
        document.body.appendChild(span);

        console.log(`Created at: ${randomLeft} (ID: ${uniqueID})`);

        setTimeout(() => {
            document.getElementById(uniqueID)?.remove();
            console.log("Removed:", uniqueID);
        }, 4999);
    }
}, 300);

