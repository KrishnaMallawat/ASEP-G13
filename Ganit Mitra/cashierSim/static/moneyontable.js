let numberOfBoxes=0;
window.service_total_amount =0;
window.payment=0;

export function putMoney(amount) {
    if(numberOfBoxes<30){
        let parent = document.querySelector(".trade_centre .service");  
        let div = document.createElement("div");

        div.classList.add("money");
        div.style = "height: 4vh; width: 5vw; background-color: green; text-align: center; margin: 5px;";
        div.textContent = amount;

        parent.appendChild(div); 

        window.service_total_amount+=amount;
        numberOfBoxes++;
    }
}
 
export function customer_payment(bill_amount){
    while(payment<bill_amount){
        const bills=[100,200,500];

        let parent = document.querySelector(".trade_centre .customer");  
        let div = document.createElement("div");

        div.classList.add("money");
        div.style = "height: 4vh; width: 5vw; background-color: green; text-align: center; margin: 5px;";
        let cash=bills[Math.floor(Math.random()*3)];
        div.textContent = cash;
        payment+=cash;

        parent.appendChild(div); 
    }
}
 