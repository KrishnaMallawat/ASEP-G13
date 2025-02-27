import { customer_payment, putMoney } from "../static/moneyontable.js";
import { nextBilling,Calculate } from "../static/machinebuttons.js";

document.querySelector(".billing").addEventListener("click", nextBilling);

document.querySelector(".enter").addEventListener("click", function(){
    Calculate(this,customer_payment);
});

document.querySelectorAll(".box_bottom").forEach(element => {
    element.addEventListener("click",function(event){
        putMoney(parseInt(event.target.textContent));
    });
});


let countdown
let totalTime=180;
let timeLeft=totalTime;

function update_time(){
    let percentage = (timeLeft / totalTime) * 100;
    document.getElementById("timeBar").style.height = percentage + "%";
}

if (!countdown) {  
    countdown = setInterval(() => {
        if (timeLeft > 0) {  
            timeLeft--;  
            update_time();  
        }
        else{
            setTimeout(() => {
                function calculateAverage(arr) {
                    if (arr.length === 0) return 0; // Avoid division by zero
                    let sum = arr.reduce((acc, val) => acc + val, 0);
                    return sum / arr.length;
                }
                
                let avg_speed = calculateAverage(window.billingTimes);

                fetch('/cashierSim/storeCustomers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        customers: window.customers, 
                        accuracy: ((window.correctClicks / window.clicks) * 100) ,
                        avg_speed : avg_speed
                    })
                }).then(() => {
                    window.location.href = "/cashierSim/end";
                });
            }, 2000);
        }
    }, 1000); 
}