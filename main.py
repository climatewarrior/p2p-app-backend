#!/usr/bin/python

from flask import Flask

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

@app.route("/login", methods=["POST"])
def login():
    pass

@app.route("/logout")
def logout():
    pass

@app.route('/questions/<question_id>')
def get_question(question_id):
    pass

@app.route('/new_answer', methods=["POST"])
def add_answser(question_id):
    pass

@app.route('/add_question', methods=['POST'])
def add_question():
    pass

if __name__ == "__main__":
    app.run(debug=True)
