window.totalBill=0;
window.customers=0;
window.clicks=-1;
window.correctClicks=-1;
window.billingTimes = []; 

let startTime=0

export function nextBilling(){

    let parent = document.querySelector(".trade_centre .customer");  
    let div = document.createElement("div");

    div.classList.add("ticket");
    div.style = "height: 18vh; width: 8vw; text-align: center; margin: 5px;";
    div.textContent = ' TICKET : '
    div.textContent += window.totalBill;

    if (window.customers>0) {
        parent.appendChild(div);

        let endTime = performance.now();
        let timeTaken = (endTime - startTime)/1000;
        window.billingTimes.push(timeTaken);
        console.log(timeTaken)
        console.log("Time taken for billing (excluding timeout):", timeTaken, "s");
    }

    console.log(window.service_total_amount);
    console.log(window.payment);
    console.log(totalBill);

    if(window.service_total_amount==window.payment-totalBill){
        let script = document.createElement("script")
        script.src = window.scriptpath
        document.body.appendChild(script);
        div.classList.add("correct"); 
        window.customers+=1;
        window.correctClicks+=1;
        startTime = performance.now();
    }
    else{
        div.classList.add("wrong");
    }

    window.clicks+=1;

    setTimeout(() => {
        document.querySelector(".ticket").remove();
        document.querySelectorAll(".money").forEach(element => {
            element.remove();
        });
        document.getElementById("totalBilled").value=0;

        window.payment=0;
        window.service_total_amount=0;
    }, 3000);
}


export function Calculate(button,customer_payment){
    let totalInput = document.getElementById("totalBilled").value;
    console.log(window.totalBill);
    console.log(totalInput);

    if (totalInput==window.totalBill){
        button.classList.add("correct"); 
        customer_payment(totalInput);
        window.correctClicks+=1;
    } else {
        button.classList.add("wrong"); 
    }

    window.clicks+=1;

    setTimeout(() => {
        button.classList.remove("correct", "wrong");
    }, 3000);
}
