#!/usr/bin/python
from flask import Flask, make_response, jsonify, request, abort, url_for, \
    render_template
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.pymongo import PyMongo
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from md5 import md5
from bson.json_util import dumps
from bson.objectid import ObjectId
from urlparse import urlparse
from datetime import date
from dateutil import parser

import datetime
import code, os, bson

app = Flask(__name__, static_url_path='')
auth = HTTPBasicAuth()
UPLOADS_DEFAULT_DEST = os.getcwd()+os.sep+'/uploads/'
app.config['UPLOADS_DEFAULT_DEST'] = UPLOADS_DEFAULT_DEST
UPLOADS_DEFAULT_URL = '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

salt = "thisCode1337Safe"

# Connect to MongoDB with the defaults
mongo = PyMongo(app)
auth = HTTPBasicAuth()

@app.route("/")
def index():
    return render_template("index.html")

@auth.get_password
def get_password(username):
    user = mongo.db.users.find_one({"username":username})
    if not user:
        return make_response(jsonify( { 'Error': 'User Not Found!' } ), 404)
    return user['password']

@app.route("/test_auth")
@auth.login_required
def test_auth():
    """
    Call this method just to see if auth token works.
    """
    return "OK\n", 200

@auth.hash_password
def hash_pw(password):
    return md5(password + salt).hexdigest()

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'Error': 'Unauthorized Access' } ), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'Error': 'Not Found' } ), 404)

@app.route("/questions", methods=['GET'])
def get_recent_questions():
    questions = mongo.db.questions.find().sort('$natural',-1).limit(10)
    list = []
    for q in questions:
        tmp = {}
        tmp['posted_epoch_time'] = convert_timestamp_to_epoch(q['_id'].generation_time)
        tmp['id'] = str(q['_id'])
        tmp['title'] = q['title']
        tmp['tags'] = q['tags']
        tmp['submitter'] = q['submitter']
        tmp['votes'] = q['votes']
        tmp['number_of_answers'] = mongo.db.answers.find({"question_id":q['_id']}).count()

        list.append(tmp)

    if not list:
        return make_response(jsonify( { 'Error': 'No Questions Found!' } ), 404)
    
    return dumps(list), 201

@app.route('/user', methods=["POST"])
def register():
    if not request.json:
        abort(400)

    data_fields = ("username", "password", "email")
    if not all(d in request.json for d in data_fields):
        abort(400)

    pw_hash = md5(request.json['password'] + salt).hexdigest()
    user = {
        'username'              : request.json['username'],
        'email'                 : request.json['email'],
        'password'              : pw_hash,
        'points'                : 0,
        'number_of_questions'   : 0,
        'number_of_answers'     : 0
    }

    mongo.db.users.insert(user)

    return make_response(jsonify( { 'Success': 'OK!' } ), 201)

# This function returns the profile of a specific user
# Points, Image
@app.route('/user/<username>', methods=["GET"])
@auth.login_required
def get_profile(username):
    user = mongo.db.users.find_one({"username":username})
    if not user:
        return make_response(jsonify( { 'Error': 'User Not Found!' } ), 404)
    
    user.pop('email')
    user.pop('password')
    user['_id'] = str(user['_id'])
    
    #profile = {}
    
    #profile['username'] = username
    #profile['number_of_questions'] = mongo.db.questions.find(
                                        #{"submitter":user['username']}).count()
    #profile['number_of_answers'] = mongo.db.answers.find(
                                        #{"submitter":user['username']}).count()
    #profile['points'] = user['points']
    
    1
    return dumps(user), 201

@app.route('/user/question', methods=["GET"])
@auth.login_required
def get_questions_for_user():
    questions = mongo.db.questions.find({"submitter":auth.username()})
    list = []
    for q in questions:
        tmp = {}
        tmp['posted_epoch_time'] = convert_timestamp_to_epoch(q['_id'].generation_time)
        tmp['id'] = str(q['_id'])
        tmp['title'] = q['title']
        tmp['tags'] = q['tags']
        tmp['submitter'] = q['submitter']
        tmp['votes'] = q['votes']
        tmp['number_of_answers'] = mongo.db.answers.find({"question_id":q['_id']}).count()

        list.append(tmp)
    
    if not list:
        return make_response(jsonify( { 'Error': 'User Has No Questions!' } ), 404)

    return dumps(list), 201

@app.route('/user/answer', methods=["GET"])
@auth.login_required
def get_answers_for_user():
    answer = mongo.db.answers.find({"submitter":auth.username()})
    list= []
    for a in answer:
        tmp = {}
        tmp['author'] = a['submitter']
        tmp['answer'] = a['content']
        tmp['votes'] = a['votes']
        tmp['_id'] = str(a['_id'])
        tmp['posted_epoch_time'] = convert_timestamp_to_epoch(a['_id'].generation_time)
        list.append(tmp)
        
    if not list:
        return make_response(jsonify( { 'Error': 'User Has No Answers!' } ), 404)

    return dumps(list), 201

#This function deals with image uploading.
@app.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        print filename

    image = {
             'username':auth.username(),
             'img_uri': 'uploads/photos/'+filename
             }
    mongo.db.images.insert(image)

    print UPLOADS_DEFAULT_DEST
    return "Successfully Uploaded\n", 201

def convert_timestamp_to_epoch(generation_time):
    epochStartTime = (datetime.datetime(1970,1,1)).replace(tzinfo=None)
    generationDatetime = (parser.parse(str(generation_time))).replace(tzinfo=None)
    generationEpochTime = (generationDatetime - epochStartTime).total_seconds()

    return int(generationEpochTime)

@app.route('/questions/<ObjectId:question_id>', methods=["GET"])
def get_question(question_id):
    question = mongo.db.questions.find_one(question_id)
    
    if not question:
        return make_response(jsonify( { 'Error': 'Question Not Found!' } ), 404)
    
    question['posted_epoch_time'] = convert_timestamp_to_epoch(question['_id'].generation_time)

    ans = mongo.db.answers.find({"question_id":question_id})
    list= []
    for a in ans:
        tmp = {}
        tmp['author'] = a['submitter']
        tmp['answer'] = a['content']
        tmp['votes'] = a['votes']
        tmp['answer_id'] = str(a['_id'])
        tmp['posted_epoch_time'] = convert_timestamp_to_epoch(a['_id'].generation_time)
        list.append(tmp)
        
    question['answers'] = list
    question['_id'] = str(question['_id'])

    return dumps(question), 201

@app.route('/questions/<ObjectId:question_id>', methods=["DELETE"])
@auth.login_required
def delete_question(question_id):
    question = mongo.db.questions.find_one(question_id)
    
    if not question:
        return make_response(jsonify( { 'Error': 'Question Not Found!' } ), 404)
    
    #If user wants to delete his answer, then remove the doc from the collection
    if 'answer' in request.json:
        ans_id = request.json['answer']['_id']
        answer = mongo.db.answers.find_one({'_id': ObjectId(ans_id)})
        if not answer:
            return make_response(jsonify( { 'Error': 'Answer Not Found!' } ), 404)
        
        #Make sure that the answer is tied to the question_id in the URL before deleting it?
        if str(question_id) != str(answer['question_id']):        
            return "The answer you want to delete does not belong to the question you are currently viewing", 403
        
        #Make sure the author of the answer is the same person who is deleting it
        if auth.username() == answer['submitter']:        
            mongo.db.answers.remove( {'_id': ObjectId(ans_id)} )
        else:
            return "You are not allowed to delete this answer\n", 403
            
    #If user wants to delete his question, then remove the doc from the collection
    elif 'question' in request.json:
        
        #Make sure the author of the question is the same who is deleting it
        if auth.username() == question['submitter']:        
            mongo.db.questions.remove( {'_id': ObjectId(question_id)} )
        else:
            return "You are not allowed to delete this question\n", 403
        
    else:
        return "Bad Request: Neither question, nor answer field in delete request\n", 400
    
    return "OK\n", 200

@app.route('/questions/<ObjectId:question_id>', methods=["PUT"])
@auth.login_required
def edit_question(question_id):
    question = mongo.db.questions.find_one(question_id)
    if not question:
        return make_response(jsonify( { 'Error': 'Question Not Found!' } ), 404)

    if 'answer' in request.json:
        answer = {
                  'question_id'  : question_id,
                  'content'      : request.json['answer'],
                  'submitter'    : auth.username(),
                  'votes'        : 0
                  }
        mongo.db.answers.insert(answer)
        
        #Increment the user's numAnswers
        mongo.db.users.update(
                              { 'username' : auth.username() },
                              { '$inc': {'number_of_answers' : 1} }
                              )
    
    #elif('accepted' in request.json):
        #if(request.json['accepted'] == 1):
            ##Change answer to accepted
            #mongo.db.questions.update(
                                      #{ '_id' : question_id },
                                      #{ '$inc': {'votes' : 1}}
                                   #   )
            #Increase asker's rep points (+5)
            #mongo.db.users.update(
                                  #{ 'username' : auth.username() },
                                  #{ '$inc': {'points' : 5}}
                                  #)
    elif 'vote' in request.json:
        if request.json['vote'] == 'up':
            #Increase question votes
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$inc': {'votes' : 1}}
                                      )

            #Increase asker's rep points (+5)
            mongo.db.users.update(
                                  { 'username' : question['submitter'] },
                                  { '$inc': {'points' : 5}}
                                  )
        elif request.json['vote'] == 'down':
            #Decrease question votes
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$inc': {'votes' : -1}}
                                      )

            #Decrease asker's rep points (-2)
            mongo.db.users.update(
                                  { 'username' : question['submitter'] },
                                  # We need to enforce unique usernames
                                  { '$inc': {'points' : -2}}
                                  )
        else:
            return "Bad Request: Vote neither up nor down\n", 400
        
    #Edit a question's title or content
    elif 'question' in request.json:
        if 'title' in request.json['question']:
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$set': {'title' : request.json['question']['title']}}
                                      )
        
        if 'detailed' in request.json['question']:
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$set': {'detailed' : request.json['question']['detailed']}}
                                      )
        
        if 'tags' in request.json['question']:
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$set': {'tags' : request.json['question']['tags']}}
                                      )

    else:
        return "Bad Request: Neither answer, nor vote, nor question fields\n", 400

    return "OK\n", 200

@app.route('/questions', methods=['POST'])
@auth.login_required
def add_question():
    print request.json
    data_fields = ("title", "detailed", "tags")
    if not all(d in request.json for d in data_fields):
        abort(400)

    question = {
        'votes'         : 0,
        'title'         : request.json['title'],
        'tags'          : request.json['tags'].split(','),
        'detailed'      : request.json['detailed'],
        'submitter'     : auth.username(),
        'images'        : {},
        'answers'       : {},
        'accepted'      : 0
    }

    id = str(mongo.db.questions.insert(question))
    question['uri'] = url_for('get_question', question_id = id, \
                              _external = True)

    #Increment the asker's numQuestions
    mongo.db.users.update(
                              { 'username' : auth.username() },
                              { '$inc': {'number_of_questions' : 1} }
                              )
    
    return dumps( { 'question': question }), 201

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
