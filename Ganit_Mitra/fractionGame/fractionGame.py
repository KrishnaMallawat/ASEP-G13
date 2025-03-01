from flask import Flask, jsonify ,render_template , Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import random
import os

fractionBp = Blueprint (
    "fractionGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@fractionBp.route('/')
@login_required
def loading():
    return render_template('fractionLoading.html')

@fractionBp.route('/home')
@login_required
def home():
    return render_template('fractionHome.html')

@fractionBp.route('/play')
@login_required
def play():
    return render_template('fractionGame.html')

@fractionBp.route('/results')
@login_required
def results():
    return render_template('fractionResult.html')