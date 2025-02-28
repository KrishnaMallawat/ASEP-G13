from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os

pictographBp = Blueprint (
    "pictographGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@pictographBp.route('/')
def loading():
    return redirect(url_for("pictographGame.home"))

@pictographBp.route('/home')
def home():
    return render_template('pictographHome.html')

@pictographBp.route('/play')
def play():
    return render_template('pictographGame.html')

@pictographBp.route('/how-to-play')
def instructions():
    return render_template('pictographInstructions.html')

@pictographBp.route('/results')
def results():
    score = request.args.get('score', 0, type=int)
    return render_template('pictographResults.html',score=score)