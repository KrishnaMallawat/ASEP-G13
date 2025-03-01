from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import json
import random
import os

caseStudyBp = Blueprint (
    "caseStudy", __name__,
    template_folder="templates",
    static_folder="static"
)

@caseStudyBp.route('/')
@login_required
def loading():
    return render_template('caseStudyLoading.html')

@caseStudyBp.route('/home')
@login_required
def home():
    return render_template('caseStudyHome.html')

@caseStudyBp.route('/chapter_selection')
@login_required
def chapter_selection():
    return render_template('caseStudyChapterSelection.html')

@caseStudyBp.route('/how-to-play')
@login_required
def instructions():
    return render_template('caseStudyInstructions.html')

@caseStudyBp.route('/chapter1')
@login_required
def chapter1():
    return render_template('chapter1.html')

@caseStudyBp.route('/chapter2')
@login_required
def chapter2():
    return render_template('chapter2.html')

@caseStudyBp.route('/chapter3')
@login_required
def chapter3():
    return render_template('chapter3.html')

@caseStudyBp.route('/chapter4')
@login_required
def chapter4():
    return render_template('chapter4.html')

@caseStudyBp.route('/chapter5')
@login_required
def chapter5():
    return render_template('chapter5.html')

@caseStudyBp.route('/chapter6')
@login_required
def chapter6():
    return render_template('chapter6.html')

@caseStudyBp.route('/play')
@login_required
def play():
    return render_template('caseStudyGame.html')

@caseStudyBp.route('/results')
@login_required
def results():
    score = request.args.get('score', 0, type=int)
    return render_template('caseStudyResults.html',score=score)