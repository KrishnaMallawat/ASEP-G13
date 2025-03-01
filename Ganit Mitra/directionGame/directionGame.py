from flask import Flask, jsonify ,render_template , redirect,url_for, Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extension import db
import json
import random
import os

directionBp = Blueprint (
    "directionGame", __name__,
    template_folder="templates",
    static_folder="static"
)

@directionBp.route('/')
@login_required
def loading():
    return render_template('directionLoading.html')

@directionBp.route('/home')
@login_required
def home():
    return render_template('directionHome.html')

@directionBp.route('/play')
@login_required
def play():
    return render_template('directionGame.html')

@directionBp.route('/how-to-play')
@login_required
def instructions():
    return render_template('directionInstructions.html')

@directionBp.route('/results')
@login_required
def results():
    score = request.args.get('score', 0, type=int)
    results = request.args.get('results')
    if results:
        results = json.loads(results)  
    else:
        results = [] 
        
    print("Received results:", results)
    return render_template('directionResults.html',score=score,results=results)