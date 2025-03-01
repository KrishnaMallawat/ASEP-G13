from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import json
import random
import os

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
    # score = request.args.get('score', 0, type=int)
    # results = request.args.get('results')
    # if results:
    #     results = json.loads(results)  
    # else:
    #     results = [] 
        
    # print("Received results:", results)
    return render_template('clockResults.html')