#!/usr/bin/python

from flask import Flask, make_response, jsonify, request, abort, url_for, \
    render_template
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.pymongo import PyMongo
from flask.ext.testing import TestCase
from md5 import md5
from bson.json_util import dumps
from urlparse import urlparse
from datetime import date

import code, os, bson

app = Flask(__name__, static_url_path='')
salt = "thisCode1337Safe"
MONGO_URL = os.environ.get('MONGOHQ_URL')
 
if MONGO_URL:
    
    # connect to Heroku MongoHQ server 
    url = urlparse(MONGO_URL)
    app.config['HEROKU_HOST'] = url.hostname
    app.config['HEROKU_PORT'] = url.port
    app.config['MONGO_USERNAME'] = url.username
    app.config['MONGO_PASSWORD'] = url.password
    app.config['HEROKU_DBNAME'] = MONGO_URL.split('/')[-1]
    mongo = PyMongo(app, config_prefix='HEROKU')
    # Get a connection
    #conn = Connection(MONGO_URL)
    
    # Get the database
    #db = conn[urlparse(MONGO_URL).path[1:]]
else:
    # connect to MongoDB with the defaults
    #connection = Connection('localhost', 27017)
    #db = connection['p2p']
    #mongo = PyMongo(app, config_prefix='HEROKU')
    mongo = PyMongo(app)

auth = HTTPBasicAuth()

@app.route("/")
def index():
    return render_template("index.html")

@auth.get_password
def get_password(username):
    user = mongo.db.users.find_one({"username":username})
    return user['password']

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
    questions = mongo.db.questions.find().sort('$natural', -1).limit(10)
    
    for question in questions:
        question['answers'].pop()
        question['images'].pop()
        question['detailed'].pop()
    
    return dumps({'questions':questions}), 201

@app.route('/register', methods=["POST"])
def register():
    if not request.json:
        abort(400)

    data_fields = ("username", "password", "email")
    if not all(d in request.json for d in data_fields):
        abort(400)

    pw_hash = md5(request.json['password'] + salt).hexdigest()
    user = {
        'username'  : request.json['username'],
        'email'     : request.json['email'],
        'password'  : pw_hash
    }

    mongo.db.users.insert(user)

    return make_response(jsonify( { 'success': 'ok!' } ), 201)

@app.route('/questions/<ObjectId:question_id>')
def get_question(question_id):
    question = mongo.db.questions.find_one(question_id)
    
    question.pop('number_of_answers')
    question.pop('submitter')
    question.pop('uri')
    question['_id'] = str(question['_id']) 

    return dumps({ 'question': question }), 201

@app.route('/questions/<ObjectId:question_id>', methods=["PUT"])
@auth.login_required
def add_answser(question_id):
    #WAIT FOR GABRIEL FOR JSON
    question = mongo.db.questions.find_one(question_id)
    question['answers'].append(request.json['answer'])
    mongo.db.questions.update(question)
    
    return "ok"

@app.route('/questions', methods=['POST'])
@auth.login_required
def add_question():
    data_fields = ("title", "detailed", "tags")
    if not all(d in request.json for d in data_fields):
        abort(400)

    #Mongo will automatically add and populate '_id' field
    question = {
        'title'             : request.json['title'],
        'tags'              : request.json['tags'],
        'detailed'          : request.json['detailed'],
        'submitter'         : '',
        'uri'               : '',
        'votes'             : 0,
        'posted-epoch-time' : 0,
        'images'            : {},
        'number_of_answers' : 0,
        'answers'           : {}
    }

    id = mongo.db.questions.insert(question)
    #question['_id'] = str(id)
    #Do we still need 'uri'?
    
    #question['uri'] = url_for('get_question', question_id = str(id), \
    #                          _external = True)
    #question['posted-epoch-time'] = id.generation_time
    
    uri_val = url_for('get_question', question_id = str(id), \
                              _external = True)
    
    #mongo.db.questions.update({'_id' : id}, {'$set' : question})
    mongo.db.questions.update({'_id' : id}, 
                    {
                     "$set" : {
                               'uri' : uri_val, 
                               'posted-epoch-time' : id.generation_time
                               }
                     })                
                    
    #mongo.db.questions.update(question)

    return dumps( { 'question': question }), 201

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)