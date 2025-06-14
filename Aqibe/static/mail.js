document.addEventListener("DOMContentLoaded", function () {
    function sendMailClick() {
        console.log('fetching');
        const email = document.querySelector("input[type='email']").value;
        fetch("/send_mail", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email }) // Send email as JSON
        })
        .then(response => response.json())

        .catch(error => console.error("Error:", error));
        console.log("fetched");
    }

    document.querySelector(".send_mail").addEventListener("click", sendMailClick);
});