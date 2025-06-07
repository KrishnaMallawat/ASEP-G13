from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from contextlib import closing
from functools import wraps

app = Flask(__name__)
app.secret_key = 'NiceTryButYouWillNotMakeIt'

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

@app.route('/game')
@login_required
def game():
    return render_template('game.html')

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
            session['username'] = username
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})
    
    data = request.get_json()
    required_fields = ['email', 'code', 'name', 'school', 'class', 'rollNumber']
    
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'})

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)