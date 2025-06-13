from flask import Flask, jsonify, render_template, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os
import sqlite3
from datetime import datetime

tbBp = Blueprint(
    "TB", __name__,
    template_folder="templates",
    static_folder="static"
)

@tbBp.route('/')
@login_required
def loading():
    return render_template('TargetLoading.html')

@tbBp.route('/instruction')
@login_required
def instruction():
    return render_template('instructions.html')

@tbBp.route('/home')
@login_required
def home():
    return render_template('index.html')

@tbBp.route('/tb/play')
@login_required
def play():
    return render_template('TBGame.html')

@tbBp.route('/tb/results')
@login_required
def results():
    return render_template('TBResults.html')

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@tbBp.before_app_request
def setup_db():
    init_db()

@tbBp.route('/tb/save_result', methods=['POST'])
@login_required
def save_result():
    data = request.get_json()
    score = data.get('score')
    total_questions = data.get('total_questions')
    if score is None or total_questions is None:
        return jsonify({'error': 'Missing data'}), 400

    db_path = os.path.join(os.path.dirname(__file__), 'results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'INSERT INTO results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
        (current_user.id, score, total_questions, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Result saved'}), 200