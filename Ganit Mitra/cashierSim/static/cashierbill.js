async function fetchData() {
    try {
        let response = await fetch("http://127.0.0.1:5000/cashierSim/data");
        
        let data = await response.json();

        let outputDiv = document.getElementsByClassName("screen")[0];
        let content = '<div style="display: flex; flex-direction: column; width: 100%;">';

        data.items.forEach(item => {
            content += `
                <div style="display: flex; justify-content: space-between; padding: 5px 10px; border-bottom: 1px solid #ccc;">
                    <span style="text-align: left;">${item.name}</span>
                    <span style="text-align: right;">${item.price}</span>
                </div>
            `;
        });

        // content += `Total: ${data.total}`;
        window.totalBill=data.total;

        outputDiv.innerHTML = content;

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

fetchData();
