from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import json
import random
import os
import sqlite3
from datetime import datetime
from flask import request, jsonify
from flask_login import login_required, current_user

clockBp = Blueprint (
    "clockGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@clockBp.route('/')
@login_required
def loading():
    return render_template('clockLoading.html')

@clockBp.route('/home')
@login_required
def home():
    return render_template('clockHome.html')

@clockBp.route('/play')
@login_required
def play():
    return render_template('clockGame.html')

@clockBp.route('/how-to-play')
@login_required
def instructions():
    return render_template('clockInstructions.html')

@clockBp.route('/results')
@login_required
def results():
    return render_template('clockResults.html')


def init_clock_db():
    db_path = os.path.join(os.path.dirname(__file__), 'clock_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clock_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@clockBp.before_app_request
def setup_clock_db():
    init_clock_db()

@clockBp.route('/save_result', methods=['POST'])
@login_required
def save_result():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug print
        print("Session contents:", dict(session))  # Debug print
        if not data:
            print("No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        score = data.get('score')
        total_questions = data.get('total_questions')
        
        print(f"Received score: {score}, total_questions: {total_questions}")  # Debug print
        
        if score is None or total_questions is None:
            print("Missing score or total_questions")
            return jsonify({'error': 'Missing data'}), 400

        user_id = session.get('username')
        print(f"User ID from session: {user_id}")  # Debug print
        
        if not user_id:
            print("User not logged in")
            return jsonify({'error': 'User not logged in'}), 401

        db_path = os.path.join(os.path.dirname(__file__), 'clock_results.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute(
            'INSERT INTO clock_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, score, total_questions, current_time)
        )
        conn.commit()
        conn.close()
        
        print("Score saved successfully")  # Debug print
        return jsonify({'message': 'Result saved successfully'}), 200
        
    except Exception as e:
        print(f"Error saving score: {e}")  # Debug print
        if 'conn' in locals():
            conn.close()
        return jsonify({'error': f'Failed to save score: {str(e)}'}), 500