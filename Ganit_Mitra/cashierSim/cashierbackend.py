from flask import Flask, jsonify ,render_template , Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import os

cashierSim = Blueprint(
    "cashierSim", __name__ ,
    template_folder="templates",
    static_folder="static"
)

app= Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///cashier_scores.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app,resources={r"/data": {"origins": "*"}})

# file_path = os.path.join(os.getcwd(),"cashierSim","items_list.txt")
file_path = os.path.join(os.path.dirname(__file__), "items_list.txt")
with open(file_path, "r", encoding="utf-8") as f:
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

@cashierSim.route("/data")
def send_q():
    selected_items = random.sample(items, random.randint(3,8))  
    total = sum(item["price"] for item in selected_items)
    bill= {
        "items":selected_items,
        "total":total,
    }
    return jsonify(bill)

@cashierSim.route('/home')
def cashier_home():
    return render_template('cashierSimHome.html') 

@cashierSim.route('/play')
def cashier_game():
    return render_template('cashier.html')

@cashierSim.route('/how-to-play')
def cashier_instructions():
    return render_template('cashierInstructions.html')

@cashierSim.route('/end')
def cashier_end():
    customers = session.get('customers', [])
    return render_template('cashierEndGame.html',customers=customers)

@cashierSim.route('/storeCustomers', methods=['POST'])
def store_customers():
    session['customers'] = request.json.get('customers', [])
    return '', 204 

if __name__ == "__main__":
    app.run(debug=True)