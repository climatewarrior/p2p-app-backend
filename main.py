#!/usr/bin/python

from flask import Flask, make_response, jsonify, request, abort
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.pymongo import PyMongo
from md5 import md5

app = Flask(__name__)

salt = "thisCode1337Safe"

# connect to MongoDB with the defaults
mongo = PyMongo(app)
auth = HTTPBasicAuth()

@app.route("/")
def hello():
    return "Hello World!"

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

    pw_hash = md5(request.json['password'] + salt).hexdigest()
    user = {'username': request.json['username'],
                'email': request.json['email'],
                'password': pw_hash}

    mongo.db.users.insert(user)

    return make_response(jsonify( { 'success': 'ok!' } ), 201)

@app.route('/questions/<ObjectId:question_id>') 
def get_question(question_id):
    question = mongo.db.questions.find_one(question_id) 
    
    return dumps( { 'question': question }), 201

@app.route('/new_answer', methods=["POST"])
@auth.login_required
def add_answser():
    return "ok"

questions = [ 
    {
        'id': 1,
        'q': u'How do you write a question in this app?',
        'ans' : [u"I don't know, man!", u"Dude, I think you just ask."]
    }
]

@app.route('/add_question', methods=['POST'])
@auth.login_required
def add_question():
    if not request.json or not 'q' in request.json or not 'ans' in \
request.json:
        abort(400)
        
    question = {
        'id': questions[-1]['id'] + 1,
        'q': request.json['q'],
        'ans': request.json['ans']
    }
    
    questions.append(question)
    return jsonify( { 'question': question } ), 201
    

if __name__ == "__main__":
    app.run(debug=True)
