from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os

casestudyBp = Blueprint (
    "casestudyGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@casestudyBp.route('/')
@login_required
def loading():
    return render_template("casestudyLoading.html")

@casestudyBp.route('/home')
@login_required
def home():
    return render_template('casestudyHome.html')

@casestudyBp.route('/select-chapter')
@login_required
def select():
    return render_template('casestudySelect.html')

@casestudyBp.route('/area-and-perimeter')
@login_required
def chapter1():
    return render_template('casestudyChapter1.html')

@casestudyBp.route('/fractions-and-decimals')
@login_required
def chapter2():
    return render_template('casestudyChapter2.html')

@casestudyBp.route('/circle')
@login_required
def chapter3():
    return render_template('casestudyChapter3.html')

@casestudyBp.route('/algebra-basics')
@login_required
def chapter4():
    return render_template('casestudyChapter4.html')

@casestudyBp.route('/data-handling')
@login_required
def chapter5():
    return render_template('casestudyChapter5.html')

@casestudyBp.route('/measurement')
@login_required
def chapter6():
    return render_template('casestudyChapter6.html')

@casestudyBp.route('/how-to-play')
@login_required
def instructions():
    return render_template('casestudyInstructions.html')

@casestudyBp.route('/results')
@login_required
def results():
    score = request.args.get('score', 0, type=int)
    return render_template('casestudyResults.html',score=score)