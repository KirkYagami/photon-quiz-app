from flask import Blueprint, render_template
from models.database import Database

main = Blueprint('main', __name__)
db = Database()

@main.route('/')
def home():
    """Home page with available quizzes"""
    quizzes = db.get_all_quizzes()
    return render_template('home.html', quizzes=quizzes)