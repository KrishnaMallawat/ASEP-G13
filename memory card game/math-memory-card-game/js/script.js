// This file contains the JavaScript functionality for the homepage of the Math Memory Card Game website.

document.addEventListener('DOMContentLoaded', () => {
    const playButton = document.getElementById('playButton');
    const howToPlayButton = document.getElementById('howToPlayButton');
    const exitButton = document.getElementById('exitButton');
    const instructionsModal = document.getElementById('instructionsModal');
    const closeModalButton = document.getElementById('closeModalButton');

    playButton.addEventListener('click', () => {
        window.location.href = 'math memory card game.html'; // Redirect to the game page
    });

    howToPlayButton.addEventListener('click', () => {
        instructionsModal.classList.toggle('hidden'); // Toggle instructions modal
    });

    exitButton.addEventListener('click', () => {
        window.location.href = 'index.html'; // Redirect to the home page
    });

    closeModalButton.addEventListener('click', () => {
        instructionsModal.classList.add('hidden'); // Hide instructions modal
    });
});