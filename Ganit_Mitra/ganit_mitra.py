from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
from extension import db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
import random

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_BINDS"] = {
    "user":"sqlite:///users.db",
    "cashier": "sqlite:///cashier_results.db"  
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PROTECTION"] = "strong"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10) 
app.secret_key="meowmeowmeow"

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model,UserMixin):
    __bind_key__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/',methods=["GET","POST"])
def login():
    error=None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            session.permanent = True
            return redirect(url_for("home"))
        else :
            error="Invalid email or password"
            return render_template('login.html',error=error)
        
    return render_template('login.html',error=error)

@app.route('/signup',methods=["GET","POST"])
def signup():
    error = None
    if request.method == "POST":
        name= request.form["name"]
        roll_number = request.form["roll_number"]
        school_name = request.form["school_name"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        
        if User.query.filter_by(email=email).first():
            error =  "User already exists!"
            return render_template('signup.html',error=error)
        
        new_user = User(name=name, roll_number=roll_number, school_name=school_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template('signup.html',error=error)

@app.route('/home')
@login_required
def home():
    return render_template('home.html') 

@app.route("/logout")
@login_required
def logout():
    logout_user()  
    return redirect(url_for("login"))

@app.route('/nigga')
def nigga():
    return ' wiwiwiwiwiw '

#Blueprints registration
from cashierSim.cashierbackend import cashierSim
app.register_blueprint(cashierSim,url_prefix="/cashierSim")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)