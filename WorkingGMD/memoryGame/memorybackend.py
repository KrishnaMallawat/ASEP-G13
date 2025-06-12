from flask import Flask, jsonify ,render_template , Blueprint, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from extension import db
import random
import os

flashCards = Blueprint (
    "flashCards", __name__,
    template_folder="templates",
    static_folder="static"
)
memoryBp = Blueprint('memory', __name__)

@flashCards.route("/")
@login_required
def loading():
    return render_template('flashCardsloading.html')

@flashCards.route("/home")
@login_required
def home():
    return render_template('flashCardshome.html')

@flashCards.route("/play")
@login_required
def play():
    return render_template('flashCards.html')

@flashCards.route("/how-to-play")
@login_required
def instructions():
    return render_template('flashCardsInstructions.html')