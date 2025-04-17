from flask import Flask, jsonify ,render_template , Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os

matchBp = Blueprint (
    "matchGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@matchBp.route('/')
@login_required
def loading():
    return render_template('matchLoading.html')

@matchBp.route('/home')
@login_required
def home():
    return render_template('matchHome.html')

@matchBp.route('/play')
@login_required
def play():
    return render_template('matchGame.html')

@matchBp.route('/results')
@login_required
def results():
    return render_template('matchResult.html')