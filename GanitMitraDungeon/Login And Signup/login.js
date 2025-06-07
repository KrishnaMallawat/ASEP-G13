// Get DOM elements
const usernameInput = document.getElementById('username');
const secretCodeInput = document.getElementById('secretCode');
const loginButton = document.getElementById('loginBtn');

// Add click event listener to login button
loginButton.addEventListener('click', handleLogin);

async function handleLogin() {
    // Get input values
    const username = usernameInput.value.trim();
    const secretCode = secretCodeInput.value.trim();

    // Basic validation
    if (!username || !secretCode) {
        alert('Please enter both username and secret code');
        return;
    }

    try {
        // Here you would typically make an API call to your backend server
        // to verify the credentials against your SQL database
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
            window.location.href = 'game.html';
        } else {
            alert('Invalid username or secret code');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

// Optional: Add enter key support for login
document.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        handleLogin();
    }
}); 