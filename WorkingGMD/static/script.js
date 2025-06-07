// Utility functions
function showError(inputId, message) {
    const input = document.getElementById(inputId);
    let errorDiv = document.getElementById(`${inputId}-error`);
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = `${inputId}-error`;
        errorDiv.className = 'error-message';
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }
    
    input.classList.toggle('error', Boolean(message));
    errorDiv.textContent = message;
    errorDiv.style.display = message ? 'block' : 'none';
}

function clearError(inputId) {
    showError(inputId, '');
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Email validation function
async function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailPattern.test(email)) {
        showError('email', "Please enter a valid email address");
        return false;
    }

    try {
        const emailInput = document.getElementById('email');
        emailInput.style.opacity = '0.7';

        const response = await fetch('/api/check-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        const data = await response.json();

        emailInput.style.opacity = '1';

        if (!data.success) {
            showError('email', data.message || 'Email already registered');
            return false;
        }

        clearError('email');
        return true;
    } catch (error) {
        console.error('Email check error:', error);
        showError('email', 'Failed to check email availability');
        return false;
    } finally {
        const emailInput = document.getElementById('email');
        emailInput.style.opacity = '1';
    }
}

// Initialize email validation
function initializeEmailValidation() {
    const emailInput = document.getElementById('email');
    if (!emailInput) return;

    // Clear any error when user starts typing
    emailInput.addEventListener('input', () => {
        clearError('email');
    });

    // Validate only when user leaves the field
    emailInput.addEventListener('blur', async (e) => {
        const value = e.target.value.trim();
        if (value) {
            await validateEmail(value);
        }
    });
}

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

    // Clear any remaining errors
    clearError('email');
    clearError('code');
    clearError('name');

    document.getElementById("step1").classList.remove("active");
    document.getElementById("step2").classList.add("active");
}

function goBack() {
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

    // Get the values from step 1
    const email = document.getElementById('email').value.trim();
    const code = document.getElementById('code').value.trim();
    const name = document.getElementById('name').value.trim();

    const submitButton = document.querySelector('button[onclick="submitForm()"]');
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Registering...';

    fetch('/api/signup', {
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
    })
    .then(response => response.json())
    .then(data => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;

        if (data.success) {
            const message = `Registration Successful!\n\nYour Details:\nName: ${name}\nEmail: ${email}\nSchool: ${school}\nClass: ${classNumber}\nRoll Number: ${roll}\n\nPlease login to continue your adventure!`;
            alert(message);  // Keep this alert as it's a success message
            window.location.href = '/login';
        } else {
            showError('email', data.message || 'Registration failed. Please try again.');
            document.getElementById("step2").classList.remove("active");
            document.getElementById("step1").classList.add("active");
        }
    })
    .catch(error => {
        console.error('Signup error:', error);
        submitButton.disabled = false;
        submitButton.textContent = originalText;
        showError('email', 'An error occurred during registration. Please try again.');
        document.getElementById("step2").classList.remove("active");
        document.getElementById("step1").classList.add("active");
    });
}

// Initialize password toggle for login page
function initializeLoginPasswordToggle() {
    const secretCodeInput = document.getElementById('secretCode');
    if (secretCodeInput) {
        const togglePassword = document.createElement('button');
        togglePassword.type = 'button';
        togglePassword.textContent = '👁️';
        togglePassword.className = 'login-password-toggle';
        togglePassword.onclick = function() {
            const type = secretCodeInput.type === 'password' ? 'text' : 'password';
            secretCodeInput.type = type;
            togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        };
        secretCodeInput.parentNode.appendChild(togglePassword);
    }
}

// Add Enter key support and initialize form
document.addEventListener('DOMContentLoaded', function() {
    // Initialize email validation
    initializeEmailValidation();

    // Initialize password toggle for signup
    const codeInput = document.getElementById('code');
    if (codeInput) {
        const togglePassword = document.createElement('button');
        togglePassword.type = 'button';
        togglePassword.textContent = '👁️';
        togglePassword.className = 'signup-password-toggle';
        togglePassword.onclick = function() {
            const type = codeInput.type === 'password' ? 'text' : 'password';
            codeInput.type = type;
            togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        };
        codeInput.parentNode.appendChild(togglePassword);
    }

    // Initialize password toggle for login
    initializeLoginPasswordToggle();

    // Step 1 fields
    const step1Fields = ['email', 'code', 'name'];
    const step2Fields = ['school', 'class', 'roll'];

    // Add enter key support for step 1
    step1Fields.forEach((fieldId, index) => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (index === step1Fields.length - 1) {
                        // If it's the last field in step 1, try to go to step 2
                        goToStep2();
                    } else {
                        // Focus the next field
                        const nextField = document.getElementById(step1Fields[index + 1]);
                        if (nextField) nextField.focus();
                    }
                }
            });
        }
    });

    // Add enter key support for step 2
    step2Fields.forEach((fieldId, index) => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (index === step2Fields.length - 1) {
                        // If it's the last field in step 2, submit the form
                        submitForm();
                    } else {
                        // Focus the next field
                        const nextField = document.getElementById(step2Fields[index + 1]);
                        if (nextField) nextField.focus();
                    }
                }
            });
        }
    });
});
