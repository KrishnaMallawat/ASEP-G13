from flask import Blueprint, render_template, jsonify, session, request
from flask_login import login_required, current_user
import os
import sqlite3
from datetime import datetime

ggBp = Blueprint(
    "gg", __name__,
    template_folder="templates",
    static_folder="static"
)

@ggBp.route('/frontpage')
@login_required
def frontpage():
    return render_template('frontpage.html')

@ggBp.route('/index')
@login_required
def index():
    return render_template('ggindex.html')

@ggBp.route('/instructions')
@login_required
def instructions():
    return render_template('gginstructions.html')

@ggBp.route('/results')
@login_required
def results():
    return render_template('results.html')

@ggBp.route('/loading')
@login_required
def loading():
    return render_template('GridLoading.html')

def init_gg_db():
    db_path = os.path.join(os.path.dirname(__file__), 'gg_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS gg_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@ggBp.before_app_request
def setup_gg_db():
    init_gg_db()

@ggBp.route('/save_result', methods=['POST'])
@login_required
def save_result():
    data = request.get_json()
    score = data.get('score')
    total_questions = data.get('total_questions')
    if score is None or total_questions is None:
        return jsonify({'error': 'Missing data'}), 400

    db_path = os.path.join(os.path.dirname(__file__), 'gg_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'INSERT INTO gg_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
        (current_user.id, score, total_questions, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Result saved'}), 200
