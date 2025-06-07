function goToStep2() {
    const email = document.getElementById("email").value.trim();
    const code = document.getElementById("code").value.trim();
    const school = document.getElementById("school").value.trim();

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    if (code === "") {
      alert("Please enter a password/code.");
      return;
    }

    if (school === "") {
      alert("School name cannot be blank.");
      return;
    }

    document.getElementById("step1").classList.remove("active");
    document.getElementById("step2").classList.add("active");
  }

  function goBack() {
    document.getElementById("step2").classList.remove("active");
    document.getElementById("step1").classList.add("active");
  }

  function submitForm() {
    const userClass = document.getElementById("class").value.trim();
    const name = document.getElementById("name").value.trim();

    const classNumber = parseInt(userClass);

    if (name === "") {
      alert("Name cannot be empty.");
      return;
    }

    if (isNaN(classNumber) || classNumber < 1 || classNumber > 12) {
      alert("Class must be a number between 1 and 12.");
      return;
    }

    // Optionally re-collect step 1 values too
    const email = document.getElementById('email').value.trim();
    const code = document.getElementById('code').value.trim();
    const school = document.getElementById('school').value.trim();

    // Success
    alert(`Submitted:\nName: ${name}\nClass: ${classNumber}\nEmail: ${email}\nSchool: ${school}`);
    window.location.href = 'login.html';
  }

  function handleLogin() {
    const email = document.getElementById("email").value.trim();
    const code = document.getElementById("code").value.trim();

    if (email && code) {
      // Save login status
      sessionStorage.setItem("loggedIn", "true");
      window.location.href = "game.html"; // Redirect to game
    } else {
      alert("Please enter both email and secret code.");
    }
  }
