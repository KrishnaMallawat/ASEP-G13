from flask import Flask, jsonify ,render_template
from flask_cors import CORS
import random

app= Flask(__name__)
CORS(app,resources={r"/data": {"origins": "*"}})

with open("items_list.txt", "r", encoding="utf-8") as f:
    paragraphs = [line.strip() for line in f if line.strip()]
    
# print(paragraphs)

items=[]
for i in range(0, len(paragraphs), 2): 
        try:
            name = paragraphs[i]
            price = float(paragraphs[i + 1]) 
            items.append({"name": name, "price": price})
        except (IndexError, ValueError): 
            continue 

@app.route("/data")
def send_q():
    selected_items = random.sample(items, random.randint(3,8))  
    total = sum(item["price"] for item in selected_items)
    bill= {
        "items":selected_items,
        "total":total,
    }
    return jsonify(bill)

@app.route('/')
def index():
    return render_template('cashier.html') 

if __name__ == "__main__":
    app.run(debug=True)