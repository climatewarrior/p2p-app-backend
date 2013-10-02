#!/usr/bin/python

from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/recent")
def get_recent_questions():
    pass

@app.route('/register', methods=["POST"])
def register():
    pass

def login():
    pass

def logout():
    pass

@app.route('/questions/<question_id>')
def get_question(question_id):
    pass

def add_answser(question_id):
    pass

@app.route('/add_question', methods=['POST'])
def add_question():
    pass

if __name__ == "__main__":
    app.run()
