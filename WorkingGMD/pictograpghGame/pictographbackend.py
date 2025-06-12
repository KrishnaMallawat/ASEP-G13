from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os
import sqlite3

pictographBp = Blueprint (
    "pictographGame", __name__,
    template_folder="templates",
    static_folder="static"
)

DB_PATH = os.path.join(os.path.dirname(__file__), 'scores.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_score(user_id, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO scores (user_id, score) VALUES (?, ?)', (user_id, score))
    conn.commit()
    conn.close()

init_db()

@pictographBp.route('/')
@login_required
def loading():
    return redirect(url_for("pictographGame.home"))

@pictographBp.route('/home')
@login_required
def home():
    return render_template('pictographHome.html')

@pictographBp.route('/play')
@login_required
def play():
    return render_template('pictographGame.html')

@pictographBp.route('/how-to-play')
@login_required
def instructions():
    return render_template('pictographInstructions.html')

@pictographBp.route('/results')
@login_required
def results():
    score = request.args.get('score', 0, type=int)
    user_id = current_user.get_id() if current_user.is_authenticated else None
    save_score(user_id, score)
    return render_template('pictographResults.html',score=score)