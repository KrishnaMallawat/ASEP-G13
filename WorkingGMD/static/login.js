// Get DOM elements
const usernameInput = document.getElementById('username');
const secretCodeInput = document.getElementById('secretCode');
const loginButton = document.getElementById('loginBtn');
const loginError = document.getElementById('login-error');
const registerPrompt = document.getElementById('register-prompt');

// Function to show error message
function showError(message, showRegisterPrompt = false) {
    loginError.textContent = message;
    loginError.style.display = 'block';
    
    if (showRegisterPrompt) {
        registerPrompt.style.display = 'block';
    } else {
        registerPrompt.style.display = 'none';
    }
}

// Function to clear error message
function clearError() {
    loginError.textContent = '';
    loginError.style.display = 'none';
    registerPrompt.style.display = 'none';
}

// Add click event listener to login button
loginButton.addEventListener('click', handleLogin);

// Clear error when user starts typing
usernameInput.addEventListener('input', clearError);
secretCodeInput.addEventListener('input', clearError);

async function handleLogin() {
    // Get input values
    const username = usernameInput.value.trim();
    const secretCode = secretCodeInput.value.trim();

    // Clear any previous errors
    clearError();

    // Basic validation
    if (!username || !secretCode) {
        showError('Please enter both username and secret code');
        return;
    }

    try {
        // Disable button and show loading state
        loginButton.disabled = true;
        loginButton.textContent = 'Logging in...';

        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                secretCode: secretCode
            })
        });

        const data = await response.json();

        if (data.success) {
            // Store the user information in localStorage or sessionStorage if needed
            localStorage.setItem('username', username);
            
            // Redirect to game page on successful login
            window.location.href = '/game';
        } else {
            showError('Invalid username or secret code', true);  // Show register prompt
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('An error occurred during login. Please try again.');
    } finally {
        // Reset button state
        loginButton.disabled = false;
        loginButton.textContent = 'Start';
    }
}

// Add enter key support for login
document.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        handleLogin();
    }
}); 