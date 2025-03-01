from flask import Flask, jsonify ,render_template , Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os

level=1

cashierSim = Blueprint(
    "cashierSim", __name__ ,
    template_folder="templates",
    static_folder="static"
)

class cashier_results(db.Model,UserMixin):
    _bind_key_ = "cashier"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    customers =db.Column(db.Integer, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    avg_speed = db.Column(db.Float, nullable=False)
    level = db.Column(db.Float, nullable=False)

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
@login_required
def send_q():
    selected_items = random.sample(items, random.randint(3+level,5+level))  
    total = sum(item["price"] for item in selected_items)
    bill= {
        "items":selected_items,
        "total":total,
    }
    return jsonify(bill)

@cashierSim.route('/home')
@login_required
def cashier_home():
    return render_template('cashierSimHome.html') 

@cashierSim.route('/play')
@login_required
def cashier_game():
    return render_template('cashier.html')

@cashierSim.route('/how-to-play')
@login_required
def cashier_instructions():
    return render_template('cashierInstructions.html')

@cashierSim.route('/end')
@login_required
def cashier_end():
    latest_result = cashier_results.query.filter_by(user_id=current_user.id).order_by(cashier_results.id.desc()).first()
    return render_template(
        'cashierEndGame.html',
        customers=latest_result.customers if latest_result else "N/A",
        accuracy=latest_result.accuracy if latest_result else "N/A",
        avg_speed=latest_result.avg_speed if latest_result else "N/A"
    )

@cashierSim.route('/storeCustomers', methods=['POST'])
@login_required
def store_customers():
    data = request.json
    
    new_entry=cashier_results(
        user_id=current_user.id,
        customers=data.get('customers', 0),
        accuracy=round(float(data.get('accuracy', 0.0)), 2), 
        avg_speed=round(float(data.get('avg_speed', 0.0)), 2),
        level=level,
    )
    
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Results stored successfully'}), 200

@cashierSim.route('/history')
@login_required
def cashier_history():
    user_results = cashier_results.query.filter_by(user_id=current_user.id).all()
    return render_template('cashierHistory.html', results=user_results)

@cashierSim.route('/whoami')
@login_required
def whoami():
    return f"Current user in cashierSim: {current_user.id}, Email: {current_user.email}"
