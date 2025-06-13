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
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TEXT NOT NULL
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
    data = request.get_json()
    score = data.get('score')
    total_questions = data.get('total_questions')
    if score is None or total_questions is None:
        return jsonify({'error': 'Missing data'}), 400

    db_path = os.path.join(os.path.dirname(__file__), 'clock_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'INSERT INTO clock_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
        (current_user.id, score, total_questions, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Result saved'}), 200