from flask import Flask, jsonify ,render_template , Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os
import sqlite3
from datetime import datetime

fractionBp = Blueprint (
    "fractionGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@fractionBp.route('/')
@login_required
def loading():
    return render_template('fractionLoading.html')

@fractionBp.route('/home')
@login_required
def home():
    return render_template('fractionHome.html')

@fractionBp.route('/play')
@login_required
def play():
    return render_template('fractionGame.html')

@fractionBp.route('/results')
@login_required
def results():
    return render_template('fractionResult.html')

def init_fraction_db():
    db_path = os.path.join(os.path.dirname(__file__), 'fraction_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS fraction_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@fractionBp.before_app_request
def setup_fraction_db():
    init_fraction_db()

@fractionBp.route('/save_result', methods=['POST'])
@login_required
def save_result():
    data = request.get_json()
    score = data.get('score')
    total_questions = data.get('total_questions')
    
    if score is None or total_questions is None:
        return jsonify({'error': 'Missing data'}), 400

    user_id = session.get('username')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    try:
        db_path = os.path.join(os.path.dirname(__file__), 'fraction_results.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            'INSERT INTO fraction_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, score, total_questions, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Score saved successfully'}), 200
    except Exception as e:
        print(f"Error saving score: {e}")
        return jsonify({'error': 'Failed to save score'}), 500