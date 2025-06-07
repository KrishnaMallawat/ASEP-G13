// Database operations and enhanced form navigation for signup
document.addEventListener('DOMContentLoaded', function() {
    // Add keypress event listeners for form navigation
    const step1Fields = ['email', 'code', 'school'];
    const step2Fields = ['name', 'class'];

    // Add enter key support for step 1
    step1Fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    const allFilled = step1Fields.every(id => 
                        document.getElementById(id).value.trim() !== ''
                    );
                    
                    if (allFilled) {
                        // If all fields are filled, go to step 2
                        goToStep2();
                    } else {
                        // Find the first empty field and focus it
                        const emptyField = step1Fields.find(id => 
                            document.getElementById(id).value.trim() === ''
                        );
                        if (emptyField) {
                            document.getElementById(emptyField).focus();
                            alert(`Please fill in the ${emptyField} field`);
                        }
                    }
                }
            });
        }
    });

    // Add enter key support for step 2
    step2Fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    const allFilled = step2Fields.every(id => 
                        document.getElementById(id).value.trim() !== ''
                    );
                    
                    if (allFilled) {
                        // If all fields are filled, submit the form
                        submitFormToDatabase();
                    } else {
                        // Find the first empty field and focus it
                        const emptyField = step2Fields.find(id => 
                            document.getElementById(id).value.trim() === ''
                        );
                        if (emptyField) {
                            document.getElementById(emptyField).focus();
                            alert(`Please fill in the ${emptyField} field`);
                        }
                    }
                }
            });
        }
    });
});

// Function to submit form data to database
async function submitFormToDatabase() {
    // Get all form data
    const formData = {
        email: document.getElementById('email').value.trim(),
        code: document.getElementById('code').value.trim(),
        school: document.getElementById('school').value.trim(),
        name: document.getElementById('name').value.trim(),
        class: document.getElementById('class').value.trim()
    };

    // Validate all fields are filled
    for (const [key, value] of Object.entries(formData)) {
        if (!value) {
            alert(`Please fill in the ${key} field`);
            document.getElementById(key).focus();
            return;
        }
    }

    try {
        // Send data to backend
        const response = await fetch('/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            // Store user data in session storage
            sessionStorage.setItem('userEmail', formData.email);
            sessionStorage.setItem('userName', formData.name);
            sessionStorage.setItem('userSchool', formData.school);
            sessionStorage.setItem('userClass', formData.class);
            
            alert('Registration successful! Redirecting to login page...');
            window.location.href = 'login.html';
        } else {
            alert(data.message || 'Registration failed. Please try again.');
        }
    } catch (error) {
        console.error('Database error:', error);
        alert('An error occurred. Please try again.');
    }
} 