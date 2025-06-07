function goToStep2() {
    const email = document.getElementById("email").value.trim();
    const code = document.getElementById("code").value.trim();
    const name = document.getElementById("name").value.trim();

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    if (code === "") {
      alert("Please enter a password/code.");
      return;
    }

    if (name === "") {
      alert("Name cannot be empty.");
      return;
    }

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

    if (school === "") {
      alert("School name cannot be empty.");
      return;
    }

    if (isNaN(classNumber) || classNumber < 4 || classNumber > 7) {
      alert("Class must be a number between 4 and 7.");
      return;
    }

    if (roll === "") {
      alert("Roll number cannot be empty.");
      return;
    }

    // Get the values from step 1
    const email = document.getElementById('email').value.trim();
    const code = document.getElementById('code').value.trim();
    const name = document.getElementById('name').value.trim();

    try {
        // Send data to Flask backend
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
            alert(data.message || 'Registration failed. Please try again.');
        }
    } catch (error) {
        console.error('Signup error:', error);
        alert('An error occurred during registration. Please try again.');
    }
  }

// Add Enter key support for both steps
document.addEventListener('DOMContentLoaded', function() {
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
