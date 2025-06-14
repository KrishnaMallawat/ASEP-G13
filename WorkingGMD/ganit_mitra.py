from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from contextlib import closing
from functools import wraps
import re
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'NiceTryButYouWillNotMakeIt'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # You must fetch the user from your DB using the user_id
    with closing(get_db()) as db:
        if db:
            user = db.execute('SELECT * FROM users WHERE email = ?', (user_id,)).fetchone()
            if user:
                return User(user['email'], user['email'])
    return None

# Create directories
for directory in ['templates', 'static']:
    os.makedirs(directory, exist_ok=True)

# Database configuration
DATABASE = os.path.join(os.path.dirname(__file__), 'Data Files', 'users.db')
SCHEMA = '''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        school TEXT NOT NULL,
        class INTEGER NOT NULL,
        roll_number TEXT NOT NULL
    )
'''

# Password validation function
def validate_password(password):
    if len(password) < 8:
        return False, "Secret code must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Secret code must have at least one capital letter"
    if not re.search(r'[0-9]', password):
        return False, "Secret code must have at least one number"
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Secret code must have at least one special character (!@#$%^&*)"
    return True, "Valid password"

def get_db():
    try:
        db_dir = os.path.join(os.path.dirname(__file__), 'Data Files')
        os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    with closing(get_db()) as db:
        if db:
            db.execute(SCHEMA)
            db.commit()

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/home')
@login_required
def home():
    user_email = session.get('username')
    name = roll_number = school = ""
    if user_email:
        with closing(get_db()) as db:
            if db:
                user = db.execute('SELECT name, roll_number, school FROM users WHERE email = ?', (user_email,)).fetchone()
                if user:
                    name = user['name']
                    roll_number = user['roll_number']
                    school = user['school']
    return render_template('home.html', name=name, roll_number=roll_number, school=school)

@app.route('/api/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    data = request.get_json()
    username = data.get('username')
    secret_code = data.get('secretCode')

    if not all([username, secret_code]):
        return jsonify({'success': False, 'message': 'Missing credentials'})

    with closing(get_db()) as db:
        if not db:
            return jsonify({'success': False, 'message': 'Database error'})
        
        user = db.execute('SELECT * FROM users WHERE email = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['code'], secret_code):
            login_user(User(username, username))
            session['username'] = username
            return jsonify({'success': True, 'redirect': url_for('home')})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
@app.route('/api/signup', methods=['POST'])
def api_signup():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    data = request.get_json()
    required_fields = ['email', 'code', 'name', 'school', 'class', 'rollNumber']
    
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'})

    # Validate password
    is_valid_password, password_message = validate_password(data['code'])
    if not is_valid_password:
        return jsonify({'success': False, 'message': password_message})

    with closing(get_db()) as db:
        if not db:
            return jsonify({'success': False, 'message': 'Database error'})
        
        if db.execute('SELECT 1 FROM users WHERE email = ?', (data['email'],)).fetchone():
            return jsonify({'success': False, 'message': 'Email already registered'})

        db.execute(
            'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
            (data['email'], generate_password_hash(data['code']), data['name'],
             data['school'], data['class'], data['rollNumber'])
        )
        db.commit()
        return jsonify({'success': True})

@app.route('/api/check-email', methods=['POST'])
def check_email():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'})
        
    with closing(get_db()) as db:
        if not db:
            return jsonify({'success': False, 'message': 'Database error'})
        
        user = db.execute('SELECT 1 FROM users WHERE email = ?', (email,)).fetchone()
        if user:
            return jsonify({'success': False, 'message': 'Email already registered'})
        
        return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

from cashierSim.cashierbackend import cashierSim
from memoryGame.memorybackend import memoryBp
from fractionGame.fractionbackend import fractionBp
from pictograpghGame.pictographbackend import pictographBp
from directionGame.directionbackend import directionBp
from clockGame.clockbackend import clockBp
from casestudyGame.casestudybackend import casestudyBp
from MatchGame.matchBackend import matchBp
from TB.tbBackend import tbBp
from gg.ggBackend import ggBp
from cafeGame.cafeBackend import cafeBp
from shapeCatcherGame.shapeCatcherBackend import shapeCatcherBp

app.register_blueprint(cashierSim, url_prefix="/cashier")
app.register_blueprint(memoryBp, url_prefix="/memory")
app.register_blueprint(fractionBp, url_prefix="/fraction")
app.register_blueprint(pictographBp, url_prefix="/pictograph")
app.register_blueprint(directionBp, url_prefix="/direction")
app.register_blueprint(clockBp, url_prefix="/samay")
app.register_blueprint(casestudyBp, url_prefix="/casestudy")
app.register_blueprint(matchBp,url_prefix='/match')
app.register_blueprint(tbBp,url_prefix='/TargrtBlitz')
app.register_blueprint(ggBp,url_prefix='/gg')
app.register_blueprint(cafeBp,url_prefix='/CafeGame')
app.register_blueprint(shapeCatcherBp,url_prefix='/ShapeCatcher')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)