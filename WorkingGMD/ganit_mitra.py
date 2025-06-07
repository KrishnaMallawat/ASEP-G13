from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Create templates and static directories if they don't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Temporary user storage (replace with database later)
users = {}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/game')
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('game.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    secret_code = data.get('secretCode')

    if username in users and check_password_hash(users[username]['code'], secret_code):
        session['username'] = username
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid username or secret code'})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    name = data.get('name')
    school = data.get('school')
    class_num = data.get('class')

    if email in users:
        return jsonify({'success': False, 'message': 'Email already registered'})

    # Hash the secret code before storing
    hashed_code = generate_password_hash(code)
    
    users[email] = {
        'code': hashed_code,
        'name': name,
        'school': school,
        'class': class_num
    }

    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)