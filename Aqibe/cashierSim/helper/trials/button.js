function addBox(clickedBox) {
    // Create a new div element for the new box
    const newBox = document.createElement("div");
  
    // Add the class 'box' to the new div
    newBox.classList.add("box");
  
    // Set the text content for the new box
    newBox.textContent = "New Box";
  
    // Insert the new box after the clicked box
    clickedBox.parentNode.insertBefore(newBox, clickedBox.nextSibling);
  
    // Optionally, you can add an event to the new box too
    newBox.onclick = function() {
      addBox(newBox); // Allows new boxes to also add another box
    };
  }
  