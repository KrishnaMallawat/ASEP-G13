// Utility functions for form validation
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

// Password validation functions
function validatePassword(password) {
    const requirements = {
        length: password.length >= 8,
        capital: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*]/.test(password)
    };

    // Update requirement indicators
    Object.keys(requirements).forEach(req => {
        const element = document.getElementById(`req-${req}`);
        if (element) {
            element.classList.toggle('valid', requirements[req]);
        }
    });

    // Update strength bar
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    
    const validCount = Object.values(requirements).filter(Boolean).length;
    
    if (validCount === 0) {
        strengthBar.className = '';
        strengthText.textContent = 'Password Strength';
    } else if (validCount <= 2) {
        strengthBar.className = 'weak';
        strengthText.textContent = 'Not Strong Enough';
    } else if (validCount === 3) {
        strengthBar.className = 'medium';
        strengthText.textContent = 'Getting Better!';
    } else {
        strengthBar.className = 'strong';
        strengthText.textContent = 'Perfect! ⭐';
    }

    return Object.values(requirements).every(Boolean);
}

function initializePasswordValidation() {
    const passwordInput = document.getElementById('code');
    if (!passwordInput) return;

    passwordInput.addEventListener('input', (e) => {
        const isValid = validatePassword(e.target.value);
        clearError('code');
        
        if (e.target.value && !isValid) {
            showError('code', 'Please make your secret code stronger');
        }
    });

    passwordInput.addEventListener('blur', (e) => {
        if (e.target.value && !validatePassword(e.target.value)) {
            showError('code', 'Your secret code needs to meet all the requirements');
        }
    });
}

// Export functions
window.showError = showError;
window.clearError = clearError;
window.validateEmail = validateEmail;
window.initializeEmailValidation = initializeEmailValidation;
window.validatePassword = validatePassword;
window.initializePasswordValidation = initializePasswordValidation; 