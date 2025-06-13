from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
import os
import sqlite3
from datetime import datetime

shapeCatcherBp = Blueprint(
    "shapeCatcher", __name__,
    template_folder="templates",
    static_folder="static"
)

@shapeCatcherBp.route('/home')
@login_required
def home():
    return render_template('ShapeCatcherHome.html')

@shapeCatcherBp.route('/play')
@login_required
def play():
    return render_template('sci.html')

@shapeCatcherBp.route('/results')
@login_required
def results():
    return render_template('ShapeCatcherResults.html')

def init_shape_catcher_db():
    db_path = os.path.join(os.path.dirname(__file__), 'shape_catcher_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS shape_catcher_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@shapeCatcherBp.before_app_request
def setup_shape_catcher_db():
    init_shape_catcher_db()

@shapeCatcherBp.route('/save_result', methods=['POST'])
@login_required
def save_result():
    data = request.get_json()
    score = data.get('score')
    total_questions = data.get('total_questions')
    if score is None or total_questions is None:
        return jsonify({'error': 'Missing data'}), 400

    db_path = os.path.join(os.path.dirname(__file__), 'shape_catcher_results.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'INSERT INTO shape_catcher_results (user_id, score, total_questions, timestamp) VALUES (?, ?, ?, ?)',
        (current_user.id, score, total_questions, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Result saved'}), 200
    (current_user.id, score, total_questions, datetime.utcnow().isoformat())
    conn.commit()
    conn.close()
    return jsonify({'message': 'Result saved'}), 200
