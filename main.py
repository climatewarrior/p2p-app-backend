#!/usr/bin/python

from flask import Flask, make_response, jsonify, request, abort, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from flaskext.bcrypt import Bcrypt

app = Flask(__name__)

# connect to MongoDB with the defaults
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()

@app.route("/")
def hello():
    return "Hello World!"

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.hash_password
def hash_pw(password):
    return bcrypt.generate_password_hash(password)

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route("/recent")
def get_recent_questions():
    pass

@app.route('/register', methods=["POST"])
def register():
    if not request.json:
        abort(400)

    data_fields = ("username", "password", "email")
    if not all(d in request.json for d in data_fields):
        abort(400)

    pw_hash = bcrypt.generate_password_hash(request.json['password'])
    user = {'username': request.json['username'],
                'email': request.json['email'],
                'password': pw_hash}

    mongo.db.users.insert(user)

    return make_response(jsonify( { 'success': 'ok!' } ), 201)

@app.route('/questions/<question_id>')
def get_question(question_id):
    pass

@app.route('/new_answer', methods=["POST"])
@auth.login_required
def add_answser(question_id):
    pass

@app.route('/add_question', methods=['POST'])
def add_question():
    if not request.json or not 'q' in request.json:
        abort(400)

    question = {
        'question': request.json['q'],
        'answers' : request.json.get('a', {})

    }

    id = str(mongo.db.questions.insert(question))
    question['uri'] = url_for('get_question', question_id = id, _external = True)

    return dumps( { 'question': question }), 201



if __name__ == "__main__":
    app.run(debug=True)
