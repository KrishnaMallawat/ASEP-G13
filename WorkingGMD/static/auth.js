// Password toggle functionality
function initializePasswordToggle(inputId, toggleClass) {
    const input = document.getElementById(inputId);
    if (input) {
        const togglePassword = document.createElement('button');
        togglePassword.type = 'button';
        togglePassword.textContent = '👁️';
        togglePassword.className = toggleClass;
        togglePassword.onclick = function() {
            const type = input.type === 'password' ? 'text' : 'password';
            input.type = type;
            togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        };
        input.parentNode.appendChild(togglePassword);
    }
}

// Initialize password toggles
function initializePasswordToggles() {
    initializePasswordToggle('code', 'signup-password-toggle');
}

// Signup step navigation
async function goToStep2() {
    const email = document.getElementById("email").value.trim();
    const code = document.getElementById("code").value.trim();
    const name = document.getElementById("name").value.trim();

    // Clear previous errors
    clearError('email');
    clearError('code');
    clearError('name');

    // Validate email first
    const isEmailValid = await validateEmail(email);
    if (!isEmailValid) {
        return;
    }

    if (code === "") {
        showError('code', "Please enter a password/code");
        return;
    }

    if (name === "") {
        showError('name', "Name cannot be empty");
        return;
    }

    // Update progress bar
    document.getElementById('signup-progress').style.width = '100%';
    
    // Switch to step 2
    document.getElementById("step1").classList.remove("active");
    document.getElementById("step2").classList.add("active");
}

function goBack() {
    // Update progress bar
    document.getElementById('signup-progress').style.width = '50%';
    
    document.getElementById("step2").classList.remove("active");
    document.getElementById("step1").classList.add("active");
}

async function submitForm() {
    const userClass = document.getElementById("class").value.trim();
    const school = document.getElementById("school").value.trim();
    const roll = document.getElementById("roll").value.trim();
    const classNumber = parseInt(userClass);

    // Clear previous errors
    clearError('school');
    clearError('class');
    clearError('roll');

    if (school === "") {
        showError('school', "School name cannot be empty");
        return;
    }

    if (isNaN(classNumber) || classNumber < 4 || classNumber > 7) {
        showError('class', "Class must be a number between 4 and 7");
        return;
    }

    if (roll === "") {
        showError('roll', "Roll number cannot be empty");
        return;
    }

    // Validate roll number is numeric
    if (!/^\d+$/.test(roll)) {
        showError('roll', "Roll number must contain only digits");
        return;
    }

    // Get the values from step 1
    const email = document.getElementById('email').value.trim();
    const code = document.getElementById('code').value.trim();
    const name = document.getElementById('name').value.trim();

    const submitButton = document.querySelector('button[onclick="submitForm()"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Registering...';

    try {
        const response = await fetch('/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                code: code,
                name: name,
                school: school,
                class: classNumber,
                rollNumber: roll
            })
        });

        const data = await response.json();

        if (data.success) {
            const message = `Registration Successful!\n\nYour Details:\nName: ${name}\nEmail: ${email}\nSchool: ${school}\nClass: ${classNumber}\nRoll Number: ${roll}\n\nPlease login to continue your adventure!`;
            alert(message);
            window.location.href = '/login';
        } else {
            showError('email', data.message || 'Registration failed. Please try again.');
            document.getElementById("step2").classList.remove("active");
            document.getElementById("step1").classList.add("active");
            document.getElementById('signup-progress').style.width = '50%';
        }
    } catch (error) {
        console.error('Signup error:', error);
        showError('email', 'An error occurred during registration. Please try again.');
        document.getElementById("step2").classList.remove("active");
        document.getElementById("step1").classList.add("active");
        document.getElementById('signup-progress').style.width = '50%';
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

// Add real-time validation for roll number
function initializeRollNumberValidation() {
    const rollInput = document.getElementById('roll');
    if (!rollInput) return;

    rollInput.addEventListener('input', () => {
        clearError('roll');
        const value = rollInput.value.trim();
        
        if (value && !/^\d+$/.test(value)) {
            showError('roll', "Roll number must contain only digits");
        }
    });
}

// Handle Enter key navigation
function handleEnterKey(event) {
    if (event.key !== 'Enter') return;
    
    const currentStep = document.querySelector('.form-section.active');
    const inputs = currentStep.querySelectorAll('input');
    const currentInput = document.activeElement;
    
    // Find the index of the current input
    const currentIndex = Array.from(inputs).indexOf(currentInput);
    
    if (currentIndex === -1) return;
    
    event.preventDefault();
    
    // If we're on step 1
    if (currentStep.id === 'step1') {
        // If we're on the last input of step 1, try to go to step 2
        if (currentIndex === inputs.length - 1) {
            goToStep2();
        } else {
            // Focus the next input
            inputs[currentIndex + 1].focus();
        }
    }
    // If we're on step 2
    else if (currentStep.id === 'step2') {
        // If we're on the last input of step 2, submit the form
        if (currentIndex === inputs.length - 1) {
            submitForm();
        } else {
            // Focus the next input
            inputs[currentIndex + 1].focus();
        }
    }
}

// Initialize keyboard navigation
function initializeKeyboardNavigation() {
    const form = document.querySelector('.scroll');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('keypress', handleEnterKey);
    });
}

// Export functions
window.goToStep2 = goToStep2;
window.goBack = goBack;
window.submitForm = submitForm;
window.initializePasswordToggles = initializePasswordToggles;
window.initializeKeyboardNavigation = initializeKeyboardNavigation;
window.initializeRollNumberValidation = initializeRollNumberValidation; 