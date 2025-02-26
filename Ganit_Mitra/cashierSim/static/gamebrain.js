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
                fetch('/cashierSim/storeCustomers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ customers: --window.customers})
                }).then(() => {
                    window.location.href = "/cashierSim/end";
                });
            }, 2000);
        }
    }, 1000); 
}