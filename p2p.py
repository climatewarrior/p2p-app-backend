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
        'points'                : 1,
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


    if user['points'] > 25:
        user['profile_image'] = 'mario_medium.jpg'
    elif user['points'] > 50:
        user['profile_image'] = 'mario_cape.jpg'
    else:
        user['profile_image'] = 'mario_small.jpg'


    user['_id'] = str(user['_id'])

    return dumps(user), 201

@app.route('/user', methods=["GET"])
@auth.login_required
def get_user_profile():
    #TODO Fix this hack
    return get_profile(auth.username())

@app.route('/user/<username>/question', methods=["GET"])
@auth.login_required
def get_questions_for_a_general_user(username):
    questions = mongo.db.questions.find({"submitter":username})
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

@app.route('/user/<username>/answer', methods=["GET"])
@auth.login_required
def get_answers_for_a_general_user(username):
    answer = mongo.db.answers.find({"submitter":username})
    list = []
    q_list = []
    
    for a in answer:
        q_id = a['question_id']
        question = mongo.db.questions.find_one(ObjectId(q_id))
        
        if not question:
            return "Question " + str(q_id) + " not found\n", 404
        
        # Check if question is already part of output
        if not str(q_id) in q_list:
            q_list.append(str(q_id))
        else:
            continue
        
        q_user = mongo.db.users.find_one({"username":str(question['submitter'])})
          
        tmp = {}
        tmp['id'] = str(question['_id'])
        tmp['title'] = question['title']
        tmp['submitter'] = q_user['username']
        tmp['submitter_user_points'] = q_user['points']
        tmp['tags'] = question['tags']
        
        list.append(tmp)

    if not list:
        return make_response(jsonify( { 'Error': 'User Has No Answers!' } ), 404)

    return dumps(list), 201

@app.route('/user/question', methods=["GET"])
@auth.login_required
def get_questions_for_logged_in_user():
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
def get_answers_for_logged_in_user():
    answer = mongo.db.answers.find({"submitter":auth.username()})
    list = []
    q_list = []
    
    for a in answer:
        q_id = a['question_id']
        question = mongo.db.questions.find_one(ObjectId(q_id))
        
        if not question:
            return "Question " + str(q_id) + " not found\n", 404
        
        # Check if question is already part of output
        if not str(q_id) in q_list:
            q_list.append(str(q_id))
        else:
            continue
        
        q_user = mongo.db.users.find_one({"username":str(question['submitter'])})
          
        tmp = {}
        tmp['id'] = str(question['_id'])
        tmp['title'] = question['title']
        tmp['submitter'] = q_user['username']
        tmp['submitter_user_points'] = q_user['points']
        tmp['tags'] = question['tags']
        
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

    return int(generationEpochTime) * 1000

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
        tmp['content'] = a['content']
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

    # If user wants to delete his answer, then remove the doc from the collection
    if 'answer' in request.json:
        ans_id = request.json['answer']['_id']
        answer = mongo.db.answers.find_one({'_id': ObjectId(ans_id)})
        if not answer:
            return make_response(jsonify( { 'Error': 'Answer Not Found!' } ), 404)

        # Make sure that the answer is tied to the question_id in the URL before deleting it?
        if str(question_id) != str(answer['question_id']):
            return "The answer you want to delete does not belong to the question you are currently viewing", 403

        # Make sure the author of the answer is the same person who is deleting it
        if auth.username() == answer['submitter']:
            mongo.db.answers.remove( {'_id': ObjectId(ans_id)} )
        else:
            return "You are not allowed to delete this answer\n", 403

    # If user wants to delete his question, then remove the doc from the collection
    elif 'question' in request.json:

        # Make sure the author of the question is the same who is deleting it
        if auth.username() == question['submitter']:
            mongo.db.questions.remove( {'_id': ObjectId(question_id)} )
        else:
            return "You are not allowed to delete this question\n", 403

    else:
        return "Bad Request: Neither question, nor answer field in delete request\n", 400

    return "OK\n", 200

# This function is for adding, editing, (up.down)-voting, and accepting answers.
# This function is also for editing and (up.down)-voting questions.

@app.route('/questions/<ObjectId:question_id>', methods=["PUT"])
@auth.login_required
def edit_question(question_id):
    
    print request.json

    question = mongo.db.questions.find_one(question_id)
    if not question:
        return make_response(jsonify( { 'Error': 'Question Not Found!' } ), 404)

    if 'answer' in request.json:

        # User wants to edit a pre-existing answer
        if 'answer_id' in request.json['answer']:
            ans_id = request.json['answer']['answer_id']
            answer = mongo.db.answers.find_one({'_id': ObjectId(ans_id)})

            if not answer:
                return make_response(jsonify( { 'Error': 'Answer Not Found!' } ), 404)

            #Make sure that the answer is tied to the question_id in the URL before deleting it?
            if str(question_id) != str(answer['question_id']):
                return "The answer you want to edit does not belong to the question you are currently viewing", 403

            # User wants to (up/down)vote the answer
            if 'vote' in request.json['answer']:
                if request.json['answer']['vote'] == 'up':
                    # Increase answer's votes
                    mongo.db.answers.update(
                                            { '_id' : ObjectId(ans_id) },
                                            { '$inc': {'votes' : 1}}
                                            )

                    # Increase answer poster's rep points (+10)
                    mongo.db.users.update(
                                          { 'username' : answer['submitter'] },
                                          { '$inc': {'points' : 10}}
                                          )

                elif request.json['answer']['vote'] == 'down':
                    # Decrease answer's votes
                    mongo.db.answers.update(
                                              { '_id' : ObjectId(ans_id) },
                                              { '$inc': {'votes' : -1}}
                                              )

                    # Decrease answer poster's rep points (-2)
                    mongo.db.users.update(
                                          { 'username' : answer['submitter'] },
                                          { '$inc': {'points' : -2}}
                                          )

                    # Decrease down-voter's rep points (-1)
                    mongo.db.users.update(
                                          { 'username' : auth.username() },
                                          { '$inc': {'points' : -1}}
                                          )
                else:
                    return "Bad Request: Vote neither up nor down\n", 400

            # User wants to edit the answer's content
            elif 'content' in request.json['answer']:
                # User is allowed to edit only if he is the author of the post
                if auth.username() == answer['submitter']:

                    new_ans = { '_id' : ObjectId(ans_id) },
                    { '$set': {'content' : request.json['answer']['content']}}
                    mongo.db.answers.update(new_ans)
                else:
                    return "You are not allowed to edit this answer\n", 403

            # User wants to (un)accept the answer
            elif 'accepted' in request.json['answer']:
                # User is allowed to (un)accept the answer only if he is the author of the question
                if auth.username() == question['submitter']:
                    accepted_val = request.json['answer']['accepted']

                    # Make sure user is changing the value to something different, otherwise... points galore!
                    if str(accepted_val) == str(answer['accepted']):
                        return "Bad Request: <Accepted> is already " + accepted_val + "\n", 400

                    if accepted_val != '1' and accepted_val != '0':
                        return "Bad Request: <Accepted> must either be 0 or 1\n", 400

                    # Edit the accepted field in the answer doc
                    mongo.db.answers.update(
                                            { '_id' : ObjectId(ans_id) },
                                            { '$set': {'accepted' : accepted_val}
                                             }
                                            )

                    # The user accepts the answer
                    if accepted_val == '1':

                        # The answer's author's points are affected only if he is not also the question's author
                        if str(question['submitter']) != str(answer['submitter']):
                            # Increase answer poster's rep points (+15)
                            mongo.db.users.update(
                                                  { 'username' : answer['submitter'] },
                                                  { '$inc': {'points' : 15}}
                                                  )

                        # Increase the acceptor's rep points (+2)
                        mongo.db.users.update(
                                              { 'username' : auth.username() },
                                              { '$inc': {'points' : 2}}
                                              )
                    # The user unaccepts the answer
                    elif accepted_val == '0':

                        # The answer's author's points are affected only if he is not also the question's author
                        if str(question['submitter']) != str(answer['submitter']):
                            # Decrease answer poster's rep points (-15)
                            mongo.db.users.update(
                                                  { 'username' : answer['submitter'] },
                                                  { '$inc': {'points' : -15}}
                                                  )

                        # Decrease the acceptor's rep points (-2)
                        mongo.db.users.update(
                                              { 'username' : auth.username() },
                                              { '$inc': {'points' : -2}}
                                              )
                    else:
                        return "Bad Request: <Accepted> must either be 0 or 1\n", 400
                else:
                    return "You are not allowed to accept this answer\n", 403
            else:
                return "Bad Request: You must either vote, accept, or edit this answer\n", 400

        # User wants to create and add an answer to the question
        elif 'content' in request.json['answer']:
            answer = {
                  'question_id'  : question_id,
                  'content'      : request.json['answer']['content'],
                  'submitter'    : auth.username(),
                  'votes'        : 0,
                  'accepted'     : 0
                  }
            mongo.db.answers.insert(answer)

            #Increment the user's numAnswers and points by 1
            mongo.db.users.update(
                              { 'username' : auth.username() },
                              { '$inc': {'number_of_answers' : 1,
                                         'points' : 1} }
                              )
        else:
            return "Bad Request: You must either create, vote, accept, or edit an answer\n", 400

    elif 'question' in request.json:

        # Vote the question up or down
        if 'vote' in request.json['question']:
            if request.json['question']['vote'] == 'up':

                # Increase question votes
                mongo.db.questions.update(
                                          { '_id' : question_id },
                                          { '$inc': {'votes' : 1}}
                                          )

                # Increase asker's rep points (+5)
                mongo.db.users.update(
                                      { 'username' : question['submitter'] },
                                      { '$inc': {'points' : 5}}
                                      )

            elif request.json['question']['vote'] == 'down':
                # Decrease question votes
                mongo.db.questions.update(
                                          { '_id' : question_id },
                                          { '$inc': {'votes' : -1}}
                                          )

                # Decrease asker's rep points (-2)
                mongo.db.users.update(
                                      { 'username' : question['submitter'] },
                                      # We need to enforce unique usernames
                                      { '$inc': {'points' : -2}}
                                      )
            else:
                return "Bad Request: Vote neither up nor down\n", 400

        # Edit a question's title
        if 'title' in request.json['question']:
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$set': {'title' : request.json['question']['title']}}
                                      )
        # Edit a question's content
        if 'detailed' in request.json['question']:
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$set': {'detailed' : request.json['question']['detailed']}}
                                      )
        # Edit a question's tags
        if 'tags' in request.json['question']:
            mongo.db.questions.update(
                                      { '_id' : question_id },
                                      { '$set': {'tags' : request.json['question']['tags']}}
                                      )

    else:
        return "Bad Request: Neither answer, nor question field\n", 400

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
    }

    id = str(mongo.db.questions.insert(question))
    question['uri'] = url_for('get_question', question_id = id, \
                              _external = True)

    #Increment the asker's numQuestions by 1 and points by 2
    mongo.db.users.update(
                              { 'username' : auth.username() },
                              { '$inc': {'number_of_questions' : 1, 
                                         'points' : 2} }
                              )

    return dumps( { 'question': question }), 201

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
