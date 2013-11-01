#!/usr/bin/python

from flask import Flask, make_response, jsonify, request, abort, url_for, \
    render_template
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.pymongo import PyMongo
from flask.ext.testing import TestCase
from md5 import md5
from bson.json_util import dumps
from urlparse import urlparse

import code, os

app = Flask(__name__, static_url_path='')
auth = HTTPBasicAuth()

salt = "thisCode1337Safe"

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    # Connect to the Heroku Mongo server
    url = urlparse(MONGO_URL)
    app.config['HEROKU_HOST'] = url.hostname
    app.config['HEROKU_PORT'] = url.port
    app.config['MONGO_USERNAME'] = url.username
    app.config['MONGO_PASSWORD'] = url.password
    app.config['HEROKU_DBNAME'] = MONGO_URL.split('/')[-1]
    mongo = PyMongo(app, config_prefix='HEROKU')

else:
    # Connect to MongoDB with the defaults
    mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template("index.html")

@auth.get_password
def get_password(username):
    user = mongo.db.users.find_one({"username":username})
    return user['password']

@app.route("/test_auth")
@auth.login_required
def test_auth():
    """
    Call this method just to see if auth token works.
    """
    return "ok", 200

@auth.hash_password
def hash_pw(password):
    return md5(password + salt).hexdigest()

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route("/questions", methods=['GET'])
def get_recent_questions():
    questions = mongo.db.questions.find().sort('$natural',-1).limit(10)
    return dumps({'question':questions}), 201

@app.route('/register', methods=["POST"])
def register():
    if not request.json:
        abort(400)

    data_fields = ("username", "password", "email")
    if not all(d in request.json for d in data_fields):
        abort(400)

    pw_hash = md5(request.json['password'] + salt).hexdigest()
    user = {'username': request.json['username'],
                'email': request.json['email'],
                'password': pw_hash}

    mongo.db.users.insert(user)

    return make_response(jsonify( { 'success': 'ok!' } ), 201)

# This function returns the profile of a specific user
@app.route('/user/<ObjectId:user_id>', methods=["GET"])
def get_profile(user_id):
    user = mongo.db.users.find_one(user_id)
    return dumps({'user':user}), 201

@app.route('/questions/<ObjectId:question_id>')
def get_question(question_id, methods=["GET"]):
    question = mongo.db.questions.find_one(question_id)

    return dumps( { 'question': question }), 201

@app.route('/questions/<ObjectId:question_id>', methods=["PUT"])
@auth.login_required
def add_answser(question_id):
    #This function needs testing !!
    question = mongo.db.questions.find_one(question_id)
    question['answers'].append(request.json['answer'])
    mongo.db.questions.update(question)
    return "ok"

@app.route('/questions', methods=['POST'])
@auth.login_required
def add_question():
    print request.json
    data_fields = ("title", "detailed", "tags")
    if not all(d in request.json for d in data_fields):
        abort(400)

    question = {
        'votes': '',
        'title': request.json['title'],
        'tags': request.json['tags'],
        'detailed': request.json['detailed'],
        'submitter': '',
        'images': {},
        'answers' : {}

    }

    id = str(mongo.db.questions.insert(question))
    question['uri'] = url_for('get_question', question_id = id, \
                              _external = True)

    return dumps( { 'question': question }), 201

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
