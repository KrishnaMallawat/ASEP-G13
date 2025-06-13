from flask import Flask, jsonify, render_template, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os
import sqlite3
from datetime import datetime

matchBp = Blueprint(
    "MatchGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@matchBp.route('/instruction')
@login_required
def instruction():
    return render_template('MatchInstruction.html')

@matchBp.route('/home')
@login_required
def home():
    return render_template('MatchOpen.html')

@matchBp.route('/play')
@login_required
def play():
    return render_template('MatchGame.html')

@matchBp.route('/results')
@login_required
def results():
    return render_template('MatchResults.html')

def init_match_db():
    db_path = os.path.join(os.path.dirname(__file__), 'match_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS match_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@matchBp.before_app_request
def setup_match_db():
    init_match_db()

@matchBp.route('/save_result', methods=['POST'])
@login_required
def save_result():
    data = request.get_json()
    score = data.get('score')
    total_questions = data.get('total_questions')
    if score is None or total_questions is None:
        return jsonify({'error': 'Missing data'}), 400

    db_path = os.path.join(os.path.dirname(__file__), 'match_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'INSERT INTO match_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
        (current_user.id, score, total_questions, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Result saved'}), 200